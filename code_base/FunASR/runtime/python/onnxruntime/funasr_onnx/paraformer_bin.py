# -*- encoding: utf-8 -*-
# Copyright FunASR (https://github.com/alibaba-damo-academy/FunASR). All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

import os.path
from pathlib import Path
from typing import List, Union, Tuple
import json

import copy
import librosa
import numpy as np

from .utils.utils import (
    CharTokenizer,
    Hypothesis,
    ONNXRuntimeError,
    OrtInferSession,
    TokenIDConverter,
    get_logger,
    read_yaml,
)
from .utils.postprocess_utils import sentence_postprocess, sentence_postprocess_sentencepiece
from .utils.frontend import WavFrontend
from .utils.timestamp_utils import time_stamp_lfr6_onnx
from .utils.utils import pad_list

logging = get_logger()


class Paraformer:
    """
    Author: Speech Lab of DAMO Academy, Alibaba Group
    Paraformer: Fast and Accurate Parallel Transformer for Non-autoregressive End-to-End Speech Recognition
    https://arxiv.org/abs/2206.08317
    """

    def __init__(
        self,
        model_dir: Union[str, Path] = None,
        batch_size: int = 1,
        device_id: Union[str, int] = "-1",
        plot_timestamp_to: str = "",
        quantize: bool = False,
        intra_op_num_threads: int = 4,
        cache_dir: str = None,
        **kwargs,
    ):
        if not Path(model_dir).exists():
            try:
                from modelscope.hub.snapshot_download import snapshot_download
            except:
                raise Exception("You are exporting model from modelscope, please install modelscope and try it again. To install modelscope, you could:\n" "\npip3 install -U modelscope\n" "For the users in China, you could install with the command:\n" "\npip3 install -U modelscope -i https://mirror.sjtu.edu.cn/pypi/web/simple")
            try:
                model_dir = snapshot_download(model_dir, cache_dir=cache_dir)
            except:
                raise Exception("model_dir must be model_name in modelscope or local path downloaded from modelscope, but is {}".format(model_dir))

        model_file = os.path.join(model_dir, "model.onnx")
        if quantize:
            model_file = os.path.join(model_dir, "model_quant.onnx")
        if not os.path.exists(model_file):
            print(".onnx does not exist, begin to export onnx")
            try:
                from funasr import AutoModel
            except:
                raise Exception("You are exporting onnx, please install funasr and try it again. To install funasr, you could:\n" "\npip3 install -U funasr\n" "For the users in China, you could install with the command:\n" "\npip3 install -U funasr -i https://mirror.sjtu.edu.cn/pypi/web/simple")

            model = AutoModel(model=model_dir)
            model_dir = model.export(type="onnx", quantize=quantize, **kwargs)

        config_file = os.path.join(model_dir, "config.yaml")
        cmvn_file = os.path.join(model_dir, "am.mvn")
        config = read_yaml(config_file)
        token_list = os.path.join(model_dir, "tokens.json")
        with open(token_list, "r", encoding="utf-8") as f:
            token_list = json.load(f)

        self.converter = TokenIDConverter(token_list)
        self.tokenizer = CharTokenizer()
        self.frontend = WavFrontend(cmvn_file=cmvn_file, **config["frontend_conf"])
        self.ort_infer = OrtInferSession(
            model_file, device_id, intra_op_num_threads=intra_op_num_threads
        )
        self.batch_size = batch_size
        self.plot_timestamp_to = plot_timestamp_to
        if "predictor_bias" in config["model_conf"].keys():
            self.pred_bias = config["model_conf"]["predictor_bias"]
        else:
            self.pred_bias = 0
        if "lang" in config:
            self.language = config["lang"]
        else:
            self.language = None

    def __call__(self, wav_content: Union[str, np.ndarray, List[str]], **kwargs) -> List:
        waveform_list = self.load_data(wav_content, self.frontend.opts.frame_opts.samp_freq)
        waveform_nums = len(waveform_list)
        asr_res = []
        for beg_idx in range(0, waveform_nums, self.batch_size):

            end_idx = min(waveform_nums, beg_idx + self.batch_size)
            feats, feats_len = self.extract_feat(waveform_list[beg_idx:end_idx])
            try:
                outputs = self.infer(feats, feats_len)
                am_scores, valid_token_lens = outputs[0], outputs[1]
                if len(outputs) == 4:
                    # for BiCifParaformer Inference
                    us_alphas, us_peaks = outputs[2], outputs[3]
                else:
                    us_alphas, us_peaks = None, None
            except ONNXRuntimeError:
                # logging.warning(traceback.format_exc())
                logging.warning("input wav is silence or noise")
                preds = [""]
            else:
                preds = self.decode(am_scores, valid_token_lens)
                if us_peaks is None:
                    for pred in preds:
                        if self.language == "en-bpe":
                            pred = sentence_postprocess_sentencepiece(pred)
                        else:
                            pred = sentence_postprocess(pred)
                        asr_res.append({"preds": pred})
                else:
                    for pred, us_peaks_ in zip(preds, us_peaks):
                        raw_tokens = pred
                        timestamp, timestamp_raw = time_stamp_lfr6_onnx(
                            us_peaks_, copy.copy(raw_tokens)
                        )
                        text_proc, timestamp_proc, _ = sentence_postprocess(
                            raw_tokens, timestamp_raw
                        )
                        # logging.warning(timestamp)
                        if len(self.plot_timestamp_to):
                            self.plot_wave_timestamp(
                                waveform_list[0], timestamp, self.plot_timestamp_to
                            )
                        asr_res.append(
                            {
                                "preds": text_proc,
                                "timestamp": timestamp_proc,
                                "raw_tokens": raw_tokens,
                            }
                        )
        return asr_res

    def plot_wave_timestamp(self, wav, text_timestamp, dest):
        # TODO: Plot the wav and timestamp results with matplotlib
        import matplotlib

        matplotlib.use("Agg")
        matplotlib.rc(
            "font", family="Alibaba PuHuiTi"
        )  # set it to a font that your system supports
        import matplotlib.pyplot as plt

        fig, ax1 = plt.subplots(figsize=(11, 3.5), dpi=320)
        ax2 = ax1.twinx()
        ax2.set_ylim([0, 2.0])
        # plot waveform
        ax1.set_ylim([-0.3, 0.3])
        time = np.arange(wav.shape[0]) / 16000
        ax1.plot(time, wav / wav.max() * 0.3, color="gray", alpha=0.4)
        # plot lines and text
        for char, start, end in text_timestamp:
            ax1.vlines(start, -0.3, 0.3, ls="--")
            ax1.vlines(end, -0.3, 0.3, ls="--")
            x_adj = 0.045 if char != "<sil>" else 0.12
            ax1.text((start + end) * 0.5 - x_adj, 0, char)
        # plt.legend()
        plotname = "{}/timestamp.png".format(dest)
        plt.savefig(plotname, bbox_inches="tight")

    def load_data(self, wav_content: Union[str, np.ndarray, List[str]], fs: int = None) -> List:
        def convert_to_wav(input_path, output_path):
            from pydub import AudioSegment
            try:
                audio = AudioSegment.from_mp3(input_path)
                audio.export(output_path, format="wav")
                print("音频文件为mp3格式，已转换为wav格式")
                
            except Exception as e:
                print(f"转换失败:{e}")

        def load_wav(path: str) -> np.ndarray:
            if not path.lower().endswith('.wav'):
                import os
                input_path = path
                path = os.path.splitext(path)[0]+'.wav'
                convert_to_wav(input_path,path) #将mp3格式转换成wav格式

            waveform, _ = librosa.load(path, sr=fs)
            return waveform

        if isinstance(wav_content, np.ndarray):
            return [wav_content]

        if isinstance(wav_content, str):
            return [load_wav(wav_content)]

        if isinstance(wav_content, list):
            return [load_wav(path) for path in wav_content]

        raise TypeError(f"The type of {wav_content} is not in [str, np.ndarray, list]")

    def extract_feat(self, waveform_list: List[np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        feats, feats_len = [], []
        for waveform in waveform_list:
            speech, _ = self.frontend.fbank(waveform)
            feat, feat_len = self.frontend.lfr_cmvn(speech)
            feats.append(feat)
            feats_len.append(feat_len)

        feats = self.pad_feats(feats, np.max(feats_len))
        feats_len = np.array(feats_len).astype(np.int32)
        return feats, feats_len

    @staticmethod
    def pad_feats(feats: List[np.ndarray], max_feat_len: int) -> np.ndarray:
        def pad_feat(feat: np.ndarray, cur_len: int) -> np.ndarray:
            pad_width = ((0, max_feat_len - cur_len), (0, 0))
            return np.pad(feat, pad_width, "constant", constant_values=0)

        feat_res = [pad_feat(feat, feat.shape[0]) for feat in feats]
        feats = np.array(feat_res).astype(np.float32)
        return feats

    def infer(self, feats: np.ndarray, feats_len: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        outputs = self.ort_infer([feats, feats_len])
        return outputs

    def decode(self, am_scores: np.ndarray, token_nums: int) -> List[str]:
        return [
            self.decode_one(am_score, token_num)
            for am_score, token_num in zip(am_scores, token_nums)
        ]

    def decode_one(self, am_score: np.ndarray, valid_token_num: int) -> List[str]:
        yseq = am_score.argmax(axis=-1)
        score = am_score.max(axis=-1)
        score = np.sum(score, axis=-1)

        # pad with mask tokens to ensure compatibility with sos/eos tokens
        # asr_model.sos:1  asr_model.eos:2
        yseq = np.array([1] + yseq.tolist() + [2])
        hyp = Hypothesis(yseq=yseq, score=score)

        # remove sos/eos and get results
        last_pos = -1
        token_int = hyp.yseq[1:last_pos].tolist()

        # remove blank symbol id, which is assumed to be 0
        token_int = list(filter(lambda x: x not in (0, 2), token_int))

        # Change integer-ids to tokens
        token = self.converter.ids2tokens(token_int)
        token = token[: valid_token_num - self.pred_bias]
        # texts = sentence_postprocess(token)
        return token


class ContextualParaformer(Paraformer):
    """
    Author: Speech Lab of DAMO Academy, Alibaba Group
    Paraformer: Fast and Accurate Parallel Transformer for Non-autoregressive End-to-End Speech Recognition
    https://arxiv.org/abs/2206.08317
    """

    def __init__(
        self,
        model_dir: Union[str, Path] = None,
        batch_size: int = 1,
        device_id: Union[str, int] = "-1",
        plot_timestamp_to: str = "",
        quantize: bool = False,
        intra_op_num_threads: int = 4,
        cache_dir: str = None,
        **kwargs,
    ):

        if not Path(model_dir).exists():
            try:
                from modelscope.hub.snapshot_download import snapshot_download
            except:
                raise Exception("You are exporting model from modelscope, please install modelscope and try it again. To install modelscope, you could:\n" "\npip3 install -U modelscope\n" "For the users in China, you could install with the command:\n" "\npip3 install -U modelscope -i https://mirror.sjtu.edu.cn/pypi/web/simple")
            try:
                model_dir = snapshot_download(model_dir, cache_dir=cache_dir)
            except:
                raise Exception("model_dir must be model_name in modelscope or local path downloaded from modelscope, but is {}".format(model_dir))

        if quantize:
            model_bb_file = os.path.join(model_dir, "model_quant.onnx")
            model_eb_file = os.path.join(model_dir, "model_eb_quant.onnx")
        else:
            model_bb_file = os.path.join(model_dir, "model.onnx")
            model_eb_file = os.path.join(model_dir, "model_eb.onnx")

        if not (os.path.exists(model_eb_file) and os.path.exists(model_bb_file)):
            print(".onnx does not exist, begin to export onnx")
            try:
                from funasr import AutoModel
            except:
                raise Exception("You are exporting onnx, please install funasr and try it again. To install funasr, you could:\n" "\npip3 install -U funasr\n" "For the users in China, you could install with the command:\n" "\npip3 install -U funasr -i https://mirror.sjtu.edu.cn/pypi/web/simple")

            model = AutoModel(model=model_dir)
            model_dir = model.export(type="onnx", quantize=quantize, **kwargs)

        config_file = os.path.join(model_dir, "config.yaml")
        cmvn_file = os.path.join(model_dir, "am.mvn")
        config = read_yaml(config_file)
        token_list = os.path.join(model_dir, "tokens.json")
        with open(token_list, "r", encoding="utf-8") as f:
            token_list = json.load(f)

        # revert token_list into vocab dict
        self.vocab = {}
        for i, token in enumerate(token_list):
            self.vocab[token] = i

        self.converter = TokenIDConverter(token_list)
        self.tokenizer = CharTokenizer()
        self.frontend = WavFrontend(cmvn_file=cmvn_file, **config["frontend_conf"])
        self.ort_infer_bb = OrtInferSession(
            model_bb_file, device_id, intra_op_num_threads=intra_op_num_threads
        )
        self.ort_infer_eb = OrtInferSession(
            model_eb_file, device_id, intra_op_num_threads=intra_op_num_threads
        )

        self.batch_size = batch_size
        self.plot_timestamp_to = plot_timestamp_to
        if "predictor_bias" in config["model_conf"].keys():
            self.pred_bias = config["model_conf"]["predictor_bias"]
        else:
            self.pred_bias = 0
        if "lang" in config:
            self.language = config["lang"]
        else:
            self.language = None

    def __call__(
        self, wav_content: Union[str, np.ndarray, List[str]], hotwords: str, **kwargs
    ) -> List:
    # def __call__(
    #     self, waveform_list:list, hotwords: str, **kwargs
    # ) -> List:
        # make hotword list
        hotwords, hotwords_length = self.proc_hotword(hotwords)
        [bias_embed] = self.eb_infer(hotwords, hotwords_length)
        # index from bias_embed
        bias_embed = bias_embed.transpose(1, 0, 2)
        _ind = np.arange(0, len(hotwords)).tolist()
        bias_embed = bias_embed[_ind, hotwords_length.tolist()]
        waveform_list = self.load_data(wav_content, self.frontend.opts.frame_opts.samp_freq)
        waveform_nums = len(waveform_list)
        asr_res = []
        for beg_idx in range(0, waveform_nums, self.batch_size):
            end_idx = min(waveform_nums, beg_idx + self.batch_size)
            feats, feats_len = self.extract_feat(waveform_list[beg_idx:end_idx])
            bias_embed = np.expand_dims(bias_embed, axis=0)
            bias_embed = np.repeat(bias_embed, feats.shape[0], axis=0)
            try:
                outputs = self.bb_infer(feats, feats_len, bias_embed)
                am_scores, valid_token_lens = outputs[0], outputs[1]

                if len(outputs) == 4:
                    # for BiCifParaformer Inference
                    us_alphas, us_peaks = outputs[2], outputs[3]
                else:
                    us_alphas, us_peaks = None, None

            except ONNXRuntimeError:
                # logging.warning(traceback.format_exc())
                logging.warning("input wav is silence or noise")
                preds = [""]
            else:
                preds = self.decode(am_scores, valid_token_lens)
                if us_peaks is None:
                    for pred in preds:
                        if self.language == "en-bpe":
                            pred = sentence_postprocess_sentencepiece(pred)
                        else:
                            pred = sentence_postprocess(pred)
                        asr_res.append({"preds": pred})
                else:
                    for pred, us_peaks_ in zip(preds, us_peaks):
                        raw_tokens = pred
                        timestamp, timestamp_raw = time_stamp_lfr6_onnx(
                            us_peaks_, copy.copy(raw_tokens)
                        )
                        text_proc, timestamp_proc, _ = sentence_postprocess(
                            raw_tokens, timestamp_raw
                        )
                        # logging.warning(timestamp)
                        if len(self.plot_timestamp_to):
                            self.plot_wave_timestamp(
                                waveform_list[0], timestamp, self.plot_timestamp_to
                            )
                        asr_res.append(
                            {
                                "preds": text_proc,
                                "timestamp": timestamp_proc,
                                "raw_tokens": raw_tokens,
                            }
                        )
        return asr_res

    def proc_hotword(self, hotwords):
        hotwords = hotwords.split(" ")
        hotwords_length = [len(i) - 1 for i in hotwords]
        hotwords_length.append(0)
        hotwords_length = np.array(hotwords_length)

        # hotwords.append('<s>')
        def word_map(word):
            hotwords = []
            for c in word:
                if c not in self.vocab.keys():
                    hotwords.append(8403)
                    logging.warning(
                        "oov character {} found in hotword {}, replaced by <unk>".format(c, word)
                    )
                else:
                    hotwords.append(self.vocab[c])
            return np.array(hotwords)

        hotword_int = [word_map(i) for i in hotwords]

        hotword_int.append(np.array([1]))
        hotwords = pad_list(hotword_int, pad_value=0, max_len=10)
        
        return hotwords, hotwords_length

    def bb_infer(
        self, feats: np.ndarray, feats_len: np.ndarray, bias_embed
    ) -> Tuple[np.ndarray, np.ndarray]:
        outputs = self.ort_infer_bb([feats, feats_len, bias_embed])
        return outputs

    def eb_infer(self, hotwords, hotwords_length):
        outputs = self.ort_infer_eb([hotwords.astype(np.int32), hotwords_length.astype(np.int32)])
        return outputs

    def decode(self, am_scores: np.ndarray, token_nums: int) -> List[str]:
        return [
            self.decode_one(am_score, token_num)
            for am_score, token_num in zip(am_scores, token_nums)
        ]

    def decode_one(self, am_score: np.ndarray, valid_token_num: int) -> List[str]:
        yseq = am_score.argmax(axis=-1)
        score = am_score.max(axis=-1)
        score = np.sum(score, axis=-1)

        # pad with mask tokens to ensure compatibility with sos/eos tokens
        # asr_model.sos:1  asr_model.eos:2
        yseq = np.array([1] + yseq.tolist() + [2])
        hyp = Hypothesis(yseq=yseq, score=score)

        # remove sos/eos and get results
        last_pos = -1
        token_int = hyp.yseq[1:last_pos].tolist()

        # remove blank symbol id, which is assumed to be 0
        token_int = list(filter(lambda x: x not in (0, 2), token_int))

        # Change integer-ids to tokens
        token = self.converter.ids2tokens(token_int)
        token = token[: valid_token_num - self.pred_bias]
        # texts = sentence_postprocess(token)
        return token


class SeacoParaformer(ContextualParaformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # no difference with contextual_paraformer in method of calling onnx models
