"""Pure-NumPy forward pass for DistilBertForSequenceClassification (HF layout), float32. Verified against frozen Phase 42 outputs."""
import numpy as np
from math import sqrt
from scipy.special import erf
from safetensors.numpy import load_file
from tokenizers import Tokenizer
class NPDistilBert:
    def __init__(self, path, max_len=512):
        self.w = load_file(f"{path}/model.safetensors"); self.tok = Tokenizer.from_file(f"{path}/tokenizer.json")
        self.tok.enable_truncation(max_len); self.max_len = max_len
    def _ln(self, x, p):
        m = x.mean(-1, keepdims=True); v = ((x - m) ** 2).mean(-1, keepdims=True)
        return (x - m) / np.sqrt(v + 1e-12) * self.w[p + ".weight"] + self.w[p + ".bias"]
    def _lin(self, x, p): return x @ self.w[p + ".weight"].T + self.w[p + ".bias"]
    def logits_one(self, text):
        ids = np.array(self.tok.encode(text).ids); L = len(ids); W = self.w
        h = W["distilbert.embeddings.word_embeddings.weight"][ids] + W["distilbert.embeddings.position_embeddings.weight"][:L]
        h = self._ln(h, "distilbert.embeddings.LayerNorm")
        for i in range(6):
            p = f"distilbert.transformer.layer.{i}."
            q = self._lin(h, p + "attention.q_lin").reshape(L, 12, 64).transpose(1, 0, 2) / sqrt(64)
            k = self._lin(h, p + "attention.k_lin").reshape(L, 12, 64).transpose(1, 0, 2)
            v = self._lin(h, p + "attention.v_lin").reshape(L, 12, 64).transpose(1, 0, 2)
            s = q @ k.transpose(0, 2, 1); s = np.exp(s - s.max(-1, keepdims=True)); s /= s.sum(-1, keepdims=True)
            a = (s @ v).transpose(1, 0, 2).reshape(L, 768)
            h = self._ln(self._lin(a, p + "attention.out_lin") + h, p + "sa_layer_norm")
            f = self._lin(h, p + "ffn.lin1"); f = 0.5 * f * (1 + erf(f / sqrt(2)))
            h = self._ln(self._lin(f, p + "ffn.lin2") + h, p + "output_layer_norm")
        c = np.maximum(self._lin(h[0], "pre_classifier"), 0)
        return self._lin(c, "classifier")
    def proba(self, texts):
        Z = np.vstack([self.logits_one(t) for t in texts]); Z = np.exp(Z - Z.max(1, keepdims=True)); return Z / Z.sum(1, keepdims=True)
