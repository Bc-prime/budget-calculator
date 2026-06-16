"""
Budget Calculator — Value-Based Pricing for Python Automation Projects
Rodrigo Córdoba · bc-prime.github.io
----------------------------------------------------------------------
Lógica de Value-Based Pricing:
  Tarifa mínima/hora = Costos fijos / Horas de trabajo mensuales
  Piso mínimo        = Horas reales IA × Tarifa mínima
  Precio sugerido    = Horas tradicionales × Tarifa mínima × Factor de valor
  Ganancia real/hora = Precio sugerido / Horas reales IA
"""

import customtkinter as ctk


# ── Tema y apariencia ──────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Paleta personalizada
DARK_BG      = "#0F1117"
SURFACE      = "#1A1D2E"
SURFACE_2    = "#22263A"
ACCENT       = "#7B5EA7"
ACCENT_LIGHT = "#9F7ED4"
TEXT_PRIMARY = "#E8E8F0"
TEXT_MUTED   = "#8A8EAA"
SUCCESS      = "#4CAF82"
WARNING      = "#E8A838"
DANGER       = "#E85454"
BORDER       = "#2E3352"


# ── Helpers ────────────────────────────────────────────────────────────────────
def make_input_card(parent, label_text, hint_text, default_value):
    """
    Crea un card de input completo (frame + label + hint + entry).
    Retorna el CTkEntry para que el caller pueda leerlo.

    FIX de responsividad: el card usa pack en vez de grid interno,
    y fill='both' + expand=True para que el entry ocupe todo el ancho
    sin importar cuánto se agrande la ventana padre.
    """
    card = ctk.CTkFrame(
        parent, fg_color=SURFACE, corner_radius=10,
        border_width=1, border_color=BORDER
    )
    # No hacemos pack/grid aquí — lo hace el caller para controlar layout

    ctk.CTkLabel(
        card,
        text=label_text,
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=TEXT_PRIMARY,
        anchor="w",
    ).pack(anchor="w", padx=16, pady=(14, 2))

    ctk.CTkLabel(
        card,
        text=hint_text,
        font=ctk.CTkFont(size=11),
        text_color=TEXT_MUTED,
        anchor="w",
    ).pack(anchor="w", padx=16)

    entry = ctk.CTkEntry(
        card,
        placeholder_text="0",
        font=ctk.CTkFont(size=15, weight="bold"),
        text_color=TEXT_PRIMARY,
        fg_color=SURFACE_2,
        border_color=BORDER,
        border_width=1,
        corner_radius=8,
        height=40,
    )
    entry.pack(fill="x", expand=True, padx=16, pady=(8, 14))
    entry.insert(0, default_value)

    return card, entry


# ── Clase principal ────────────────────────────────────────────────────────────
class BudgetCalculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Budget Calculator · Value-Based Pricing")
        self.geometry("760x820")
        self.minsize(680, 780)
        self.configure(fg_color=DARK_BG)

        # Centrar ventana al abrir
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 760) // 2
        y = (self.winfo_screenheight() - 820) // 2
        self.geometry(f"+{x}+{y}")

        self._build_ui()

    # ── Construcción de la UI ──────────────────────────────────────────────────
    def _build_ui(self):
        """
        Estructura raíz:
          CTkScrollableFrame (main_frame) — scroll vertical, fill both
            └─ todos los widgets hijos usan pack(fill="x")
        """
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=DARK_BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        self.main_frame.pack(fill="both", expand=True)

        self._build_header()
        self._build_inputs_section()
        self._build_factor_section()
        self._build_calculate_button()
        self._build_results_section()

    # ── Header ─────────────────────────────────────────────────────────────────
    def _build_header(self):
        header = ctk.CTkFrame(self.main_frame, fg_color=SURFACE, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="💼  Budget Calculator",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=(22, 2))

        ctk.CTkLabel(
            header,
            text="Value-Based Pricing · Python Automation Projects",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=ACCENT_LIGHT,
        ).pack(pady=(0, 22))

        # Franja de acento violeta debajo del header
        ctk.CTkFrame(self.main_frame, height=3, fg_color=ACCENT, corner_radius=0).pack(fill="x")

    # ── Sección de inputs ──────────────────────────────────────────────────────
    def _build_inputs_section(self):
        """
        Layout de 2 columnas implementado con pack lateral (side=LEFT/RIGHT)
        dentro de filas explícitas. Esto es mucho más estable que .grid()
        dentro de CTkScrollableFrame al redimensionar.

        Estructura:
          section (fill=x)
            ├─ title label
            ├─ row_1 (fill=x)  → card_left (fill=both, expand) + card_right (fill=both, expand)
            └─ row_2 (fill=x)  → card_left (fill=both, expand) + card_right (fill=both, expand)
        """
        section = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        section.pack(fill="x", padx=40, pady=(28, 0))

        ctk.CTkLabel(
            section,
            text="📊  Datos del proyecto",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 14))

        self.entries = {}

        # Datos de los 4 inputs: (label, hint, key, default)
        inputs_data = [
            ("💵  Costos fijos mensuales",  "USD · Alquiler, suscripciones, servicios...", "costs",       "800"),
            ("⏱  Horas de trabajo/mes",     "Horas reales disponibles para proyectos",     "hours_month", "100"),
            ("🕐  Horas estimadas (sin IA)", "Estimación tradicional del proyecto",         "hours_trad",  "20"),
            ("🤖  Horas reales (con IA)",    "Tiempo real usando herramientas de IA",       "hours_ai",    "8"),
        ]

        # Fila 1: inputs[0] y inputs[1]
        # Fila 2: inputs[2] y inputs[3]
        for row_idx in range(2):
            row_frame = ctk.CTkFrame(section, fg_color="transparent")
            row_frame.pack(fill="x", pady=(0, 8))

            for col_idx in range(2):
                data_idx = row_idx * 2 + col_idx
                label_text, hint, key, default = inputs_data[data_idx]

                card, entry = make_input_card(row_frame, label_text, hint, default)

                # pack lateral: izquierda y derecha con gap entre ellas
                if col_idx == 0:
                    card.pack(side="left", fill="both", expand=True, padx=(0, 6))
                else:
                    card.pack(side="left", fill="both", expand=True, padx=(6, 0))

                self.entries[key] = entry

    # ── Slider factor de valor ─────────────────────────────────────────────────
    def _build_factor_section(self):
        """Slider 1.0 → 2.5 con etiquetas de referencia."""
        section = ctk.CTkFrame(
            self.main_frame, fg_color=SURFACE,
            corner_radius=10, border_width=1, border_color=BORDER
        )
        section.pack(fill="x", padx=40, pady=(14, 0))

        # Fila superior: título + valor numérico
        top = ctk.CTkFrame(section, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(16, 4))

        ctk.CTkLabel(
            top,
            text="⚡  Factor de Valor / Complejidad",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        self.factor_label = ctk.CTkLabel(
            top,
            text="1.50×",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=ACCENT_LIGHT,
        )
        self.factor_label.pack(side="right")

        # Slider
        slider_frame = ctk.CTkFrame(section, fg_color="transparent")
        slider_frame.pack(fill="x", padx=20)

        self.factor_slider = ctk.CTkSlider(
            slider_frame,
            from_=1.0,
            to=2.5,
            number_of_steps=30,
            command=self._on_factor_change,
            button_color=ACCENT,
            button_hover_color=ACCENT_LIGHT,
            progress_color=ACCENT,
            fg_color=BORDER,
        )
        self.factor_slider.set(1.5)
        self.factor_slider.pack(fill="x", pady=(4, 6))

        # Etiquetas de referencia debajo del slider
        refs = ctk.CTkFrame(slider_frame, fg_color="transparent")
        refs.pack(fill="x", pady=(0, 14))

        hints = [
            ("1.0×", "Tarea simple\nsin urgencia"),
            ("1.5×", "Proyecto\nestándar"),
            ("2.0×", "Alta complejidad\no urgencia"),
            ("2.5×", "Valor crítico\npara el negocio"),
        ]
        for val, desc in hints:
            col = ctk.CTkFrame(refs, fg_color="transparent")
            col.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(
                col, text=val,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=ACCENT_LIGHT,
            ).pack()
            ctk.CTkLabel(
                col, text=desc,
                font=ctk.CTkFont(size=10),
                text_color=TEXT_MUTED,
                justify="center",
            ).pack()

    def _on_factor_change(self, value):
        """Actualiza el label del slider en tiempo real."""
        self.factor_label.configure(text=f"{value:.2f}×")

    # ── Botón calcular ─────────────────────────────────────────────────────────
    def _build_calculate_button(self):
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=24)

        self.error_label = ctk.CTkLabel(
            btn_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=DANGER,
        )
        self.error_label.pack(pady=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text="  Calcular Presupuesto  →",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_LIGHT,
            text_color="#FFFFFF",
            corner_radius=10,
            height=48,
            width=280,
            command=self._calculate,
        ).pack()

    # ── Sección de resultados ──────────────────────────────────────────────────
    def _build_results_section(self):
        """
        Panel de resultados — creado pero NO empaquetado (visible=False).
        Se muestra la primera vez que el usuario calcula.
        Igual que los inputs, los dos cards secundarios usan pack lateral.
        """
        self.results_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        # .pack() se llama en _calculate() la primera vez

        ctk.CTkLabel(
            self.results_frame,
            text="📈  Resultados del presupuesto",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=40, pady=(0, 14))

        # ── Card principal: precio sugerido ────────────────────────────────────
        self.price_card = ctk.CTkFrame(
            self.results_frame,
            fg_color=SURFACE,
            corner_radius=14,
            border_width=2,
            border_color=ACCENT,
        )
        self.price_card.pack(fill="x", padx=40, pady=(0, 12))

        ctk.CTkLabel(
            self.price_card,
            text="PRECIO SUGERIDO AL CLIENTE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=ACCENT_LIGHT,
        ).pack(pady=(18, 4))

        self.price_value = ctk.CTkLabel(
            self.price_card,
            text="$0.00",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="#FFFFFF",
        )
        self.price_value.pack()

        self.price_formula = ctk.CTkLabel(
            self.price_card,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED,
        )
        self.price_formula.pack(pady=(2, 18))

        # ── Cards secundarios: piso mínimo + ganancia/hora ─────────────────────
        # Misma técnica que en los inputs: pack lateral dentro de un row_frame
        row = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        row.pack(fill="x", padx=40, pady=(0, 12))

        # Piso mínimo
        floor_card = ctk.CTkFrame(
            row, fg_color=SURFACE, corner_radius=12,
            border_width=1, border_color=BORDER
        )
        floor_card.pack(side="left", fill="both", expand=True, padx=(0, 6))

        ctk.CTkLabel(
            floor_card,
            text="🔒  PISO MÍNIMO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=WARNING,
        ).pack(pady=(16, 4))

        self.floor_value = ctk.CTkLabel(
            floor_card,
            text="$0.00",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=WARNING,
        )
        self.floor_value.pack()

        ctk.CTkLabel(
            floor_card,
            text="Costo base del tiempo real",
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED,
        ).pack(pady=(2, 16))

        # Ganancia real/hora
        gain_card = ctk.CTkFrame(
            row, fg_color=SURFACE, corner_radius=12,
            border_width=1, border_color=BORDER
        )
        gain_card.pack(side="left", fill="both", expand=True, padx=(6, 0))

        ctk.CTkLabel(
            gain_card,
            text="🚀  GANANCIA REAL / HORA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=SUCCESS,
        ).pack(pady=(16, 4))

        self.gain_value = ctk.CTkLabel(
            gain_card,
            text="$0.00 /hr",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=SUCCESS,
        )
        self.gain_value.pack()

        ctk.CTkLabel(
            gain_card,
            text="Eficiencia gracias a la IA",
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED,
        ).pack(pady=(2, 16))

        # ── Desglose detallado ─────────────────────────────────────────────────
        self.breakdown_frame = ctk.CTkFrame(
            self.results_frame, fg_color=SURFACE_2, corner_radius=10
        )
        self.breakdown_frame.pack(fill="x", padx=40, pady=(0, 28))

        ctk.CTkLabel(
            self.breakdown_frame,
            text="Desglose del cálculo",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", padx=20, pady=(14, 8))

        self.breakdown_labels = []
        for _ in range(5):
            lbl = ctk.CTkLabel(
                self.breakdown_frame,
                text="",
                font=ctk.CTkFont(size=12),
                text_color=TEXT_MUTED,
                justify="left",
                anchor="w",
            )
            lbl.pack(anchor="w", fill="x", padx=20, pady=2)
            self.breakdown_labels.append(lbl)

        ctk.CTkFrame(self.breakdown_frame, height=12, fg_color="transparent").pack()

    # ── Validación ─────────────────────────────────────────────────────────────
    def _get_validated_inputs(self):
        """
        Lee los 4 campos, valida que sean números positivos coherentes.
        Retorna dict con floats o None si hay error.
        """
        labels_map = {
            "costs":       "Costos fijos mensuales",
            "hours_month": "Horas de trabajo/mes",
            "hours_trad":  "Horas estimadas (sin IA)",
            "hours_ai":    "Horas reales (con IA)",
        }

        # Verificar que no estén vacíos
        raw = {}
        for key, entry in self.entries.items():
            val = entry.get().strip()
            if not val:
                self._show_error(f"⚠  El campo «{labels_map[key]}» está vacío.")
                return None
            raw[key] = val

        # Convertir a float (acepta coma decimal además de punto)
        parsed = {}
        for key, val in raw.items():
            try:
                parsed[key] = float(val.replace(",", "."))
            except ValueError:
                self._show_error(f"⚠  «{labels_map[key]}» debe ser un número válido.")
                return None

        # Validaciones lógicas
        if parsed["hours_month"] <= 0:
            self._show_error("⚠  Las horas de trabajo/mes deben ser mayores a 0.")
            return None
        if parsed["hours_ai"] <= 0:
            self._show_error("⚠  Las horas reales con IA deben ser mayores a 0.")
            return None
        if parsed["hours_ai"] > parsed["hours_trad"]:
            self._show_error("⚠  Las horas con IA no pueden superar las horas tradicionales.")
            return None

        return parsed

    # ── Cálculo principal ──────────────────────────────────────────────────────
    def _calculate(self):
        """Aplica las fórmulas de Value-Based Pricing y actualiza los resultados."""
        self._clear_error()
        data = self._get_validated_inputs()
        if data is None:
            return

        factor = self.factor_slider.get()

        # Tarifa mínima: cuánto vale cada hora para cubrir costos fijos
        min_rate = data["costs"] / data["hours_month"]

        # Piso mínimo: costo base si solo cobraramos las horas reales de trabajo
        floor_price = data["hours_ai"] * min_rate

        # Precio sugerido: cobras las horas tradicionales × tarifa × factor de valor
        suggested_price = data["hours_trad"] * min_rate * factor

        # Ganancia real por hora: lo que ganás por cada hora que realmente trabajaste
        real_gain_per_hour = suggested_price / data["hours_ai"]

        # Actualizar UI
        self.price_value.configure(text=f"${suggested_price:,.2f}")
        self.price_formula.configure(
            text=f"{data['hours_trad']:.0f} hs trad. × ${min_rate:.2f}/hr × {factor:.2f}× factor"
        )
        self.floor_value.configure(text=f"${floor_price:,.2f}")
        self.gain_value.configure(text=f"${real_gain_per_hour:,.2f} /hr")

        # Desglose
        breakdown_data = [
            ("Tarifa mínima",       f"${data['costs']:.0f} ÷ {data['hours_month']:.0f} hs = ${min_rate:.2f} /hr"),
            ("Piso mínimo",         f"{data['hours_ai']:.1f} hs × ${min_rate:.2f} = ${floor_price:.2f}"),
            ("Precio sugerido",     f"{data['hours_trad']:.0f} hs × ${min_rate:.2f} × {factor:.2f} = ${suggested_price:.2f}"),
            ("Ganancia real/hora",  f"${suggested_price:.2f} ÷ {data['hours_ai']:.1f} hs = ${real_gain_per_hour:.2f}/hr"),
            ("Eficiencia IA",       f"Cobrás {data['hours_trad']/data['hours_ai']:.1f}× tu tiempo real invertido"),
        ]
        for lbl, (key, val) in zip(self.breakdown_labels, breakdown_data):
            lbl.configure(text=f"  {key}:  {val}")

        # Mostrar resultados si estaban ocultos
        if not self.results_frame.winfo_ismapped():
            self.results_frame.pack(fill="x")
            self.after(60, lambda: self.main_frame._parent_canvas.yview_moveto(1.0))

        self._pulse_price_card()

    # ── Animación ──────────────────────────────────────────────────────────────
    def _pulse_price_card(self, current=0):
        """Pulso de borde violeta al mostrar el resultado."""
        colors = [ACCENT_LIGHT, ACCENT, ACCENT_LIGHT, ACCENT, ACCENT_LIGHT, ACCENT]
        if current < len(colors):
            self.price_card.configure(border_color=colors[current])
            self.after(80, lambda: self._pulse_price_card(current + 1))

    def _show_error(self, msg: str):
        self.error_label.configure(text=msg)

    def _clear_error(self):
        self.error_label.configure(text="")


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = BudgetCalculator()
    app.mainloop()
