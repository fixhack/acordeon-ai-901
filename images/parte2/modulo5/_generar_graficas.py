"""Gráficas del Tema 3 (Parte 2, Módulo 5). Ejecutar: python _generar_graficas.py
Precios de lista por imagen (USD, oct-2026) según la documentación pública de los modelos; úsalos como orden de magnitud."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#b8b8b3", "axes.labelcolor": "#444", "xtick.color": "#444",
                     "ytick.color": "#444", "figure.dpi": 160})

# 1) Costo por imagen 1024x1024 por modelo y calidad
modelos = ["gpt-image-1-mini", "gpt-image-1.5", "gpt-image-1"]
precios = {"low": [0.005, 0.009, 0.011], "medium": [0.011, 0.034, 0.042], "high": [0.036, 0.133, 0.167]}
colores = {"low": "#9ec5f4", "medium": "#5598e7", "high": "#1c5cab"}
fig, ax = plt.subplots(figsize=(9, 4.2))
x = np.arange(len(modelos)); w = 0.26
for i, (q, vals) in enumerate(precios.items()):
    bars = ax.bar(x + (i - 1) * w, vals, w - 0.03, color=colores[q], label=f"quality={q}")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.003, f"\\${v:.3f}", ha="center", fontsize=8, color="#333")
ax.set_xticks(x); ax.set_xticklabels(modelos)
ax.set_ylabel("USD por imagen 1024×1024"); ax.legend(frameon=False)
ax.set_title("Precio por imagen: la calidad pesa más que el modelo (high ≈ 15× low)", loc="left", fontsize=11)
ax.grid(axis="y", color="#e6e6e2"); ax.set_axisbelow(True)
fig.text(0.01, -0.02, "1024×1536 y 1536×1024 cuestan ~1.5× más. Precios de lista aproximados; confírmalos en la calculadora de Azure.", fontsize=7.5, color="#666")
fig.tight_layout(); fig.savefig(OUT / "costo-por-imagen.png", bbox_inches="tight"); plt.close(fig)

# 2) Tokens de salida por imagen según calidad y tamaño
calidades = ["low", "medium", "high"]
tok_1024 = [272, 1056, 4160]
tok_portrait = [408, 1584, 6240]
fig, ax = plt.subplots(figsize=(9, 3.8))
x = np.arange(3); w = 0.36
b1 = ax.bar(x - w/2, tok_1024, w - 0.03, color=AQUA, label="1024×1024")
b2 = ax.bar(x + w/2, tok_portrait, w - 0.03, color=NARANJA, label="1024×1536 / 1536×1024")
for bs in (b1, b2):
    for b in bs:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 80, f"{int(b.get_height()):,}", ha="center", fontsize=8, color="#333")
ax.set_xticks(x); ax.set_xticklabels([f"quality={c}" for c in calidades])
ax.set_ylabel("tokens de imagen de salida"); ax.legend(frameon=False)
ax.set_title("Una imagen se cobra en tokens: más calidad y más píxeles = más tokens y más latencia", loc="left", fontsize=11)
ax.grid(axis="y", color="#e6e6e2"); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(OUT / "tokens-por-imagen.png", bbox_inches="tight"); plt.close(fig)

# 3) Ilustración de edición con máscara (imagen → máscara con alfa → región editable)
rng = np.random.default_rng(3)
H = W = 256
yy, xx = np.mgrid[0:H, 0:W]
cielo = np.stack([np.full((H, W), 0.55), np.full((H, W), 0.75), np.full((H, W), 0.95)], -1)
cielo[yy > 170] = [0.85, 0.75, 0.55]                       # arena
sol = ((xx - 200) ** 2 + (yy - 60) ** 2) < 28 ** 2
cielo[sol] = [1.0, 0.85, 0.3]
img = np.clip(cielo + rng.normal(0, 0.01, cielo.shape), 0, 1)
mask_alpha = np.ones((H, W))
region = ((xx - 110) ** 2 + (yy - 200) ** 2) < 45 ** 2     # zona a editar → alfa 0
mask_alpha[region] = 0
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.4))
axs[0].imshow(img); axs[0].set_title("image: PNG original", fontsize=9)
axs[1].imshow(np.dstack([np.zeros((H, W, 3)), 1 - mask_alpha]), cmap=None)
axs[1].imshow(img, alpha=0.25); axs[1].set_title("mask: PNG con canal alfa\n(alfa = 0 → zona editable)", fontsize=9)
img2 = img.copy()
pelota = ((xx - 110) ** 2 + (yy - 200) ** 2) < 30 ** 2
img2[pelota] = [0.9, 0.2, 0.2]
franja = pelota & (((xx - 110) // 12) % 2 == 0)
img2[franja] = [1.0, 1.0, 1.0]
axs[2].imshow(img2); axs[2].set_title('resultado con prompt\n"una pelota de playa en la arena"', fontsize=9)
for a in axs: a.axis("off")
fig.suptitle("Edición con máscara (images.edit): solo cambia donde la máscara es transparente", fontsize=11, x=0.01, ha="left", y=1.04)
fig.tight_layout(); fig.savefig(OUT / "edicion-con-mascara.png", bbox_inches="tight"); plt.close(fig)

# 4) Tamaño en bytes: PNG vs JPEG vs base64
fig, ax = plt.subplots(figsize=(9, 2.9))
cats = ["PNG 1024×1024\n(output_format=png)", "JPEG calidad 80\n(output_format=jpeg,\noutput_compression=80)", "PNG en base64\n(lo que viaja en el JSON)"]
vals = [1.9, 0.25, 1.9 * 4 / 3]
bars = ax.barh(cats, vals, color=[AQUA, AQUA, NARANJA], height=0.55)
for b, v in zip(bars, vals):
    ax.text(v + 0.03, b.get_y() + b.get_height()/2, f"≈ {v:.2f} MB", va="center", fontsize=9, color="#333")
ax.set_xlabel("MB (ejemplo típico de una ilustración)"); ax.invert_yaxis()
ax.set_title("base64 infla ~33 %: decodifica al guardar y usa JPEG cuando no necesites transparencia", loc="left", fontsize=11)
ax.grid(axis="x", color="#e6e6e2"); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(OUT / "png-jpeg-base64.png", bbox_inches="tight"); plt.close(fig)
print("OK:", sorted(p.name for p in OUT.glob("*.png")))
