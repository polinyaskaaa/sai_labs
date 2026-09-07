import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
RESULTS_PATH = BASE_DIR / "model_results.csv"
METADATA_PATH = BASE_DIR / "metadata.json"


class FlightPriceApp:

    BG = "#0B1120"
    PANEL = "#111827"
    PANEL_2 = "#172033"
    CARD = "#1E293B"
    BORDER = "#334155"
    TEXT = "#E5E7EB"
    MUTED = "#94A3B8"
    ACCENT = "#38BDF8"
    ACCENT_2 = "#0EA5E9"
    SUCCESS = "#34D399"

    def __init__(self, root):
        self.root = root
        self.root.title("Flight Price Prediction")
        self.root.geometry("1500x860")
        self.root.minsize(1180, 720)
        self.root.configure(bg=self.BG)

        self.metadata = self.load_metadata()
        self.results_df = self.load_results()
        self.loaded_models = {}

        self.model_files = self.metadata["model_files"]
        self.model_names = list(self.model_files.keys())

        self.setup_styles()
        self.build_interface()

    # ========================================================
    # ЗАВАНТАЖЕННЯ ДАНИХ ПРО НАВЧЕНІ МОДЕЛІ
    # ========================================================

    def load_metadata(self):
        if not METADATA_PATH.exists():
            messagebox.showerror(
                "Моделі ще не підготовлені",
                "Не знайдено metadata.json.\n\n"
                "Спочатку один раз запустіть train_models.py."
            )
            raise SystemExit

        with open(METADATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_results(self):
        if RESULTS_PATH.exists():
            return pd.read_csv(RESULTS_PATH)
        return pd.DataFrame()

    def get_model(self, model_name):
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        model_path = MODELS_DIR / self.model_files[model_name]

        if not model_path.exists():
            raise FileNotFoundError(
                f"Не знайдено файл моделі:\n{model_path}\n\n"
                "Запустіть train_models.py."
            )

        model = joblib.load(model_path)
        self.loaded_models[model_name] = model
        return model

    # ========================================================
    # СТИЛІ
    # ========================================================

    def setup_styles(self):
        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "App.TFrame",
            background=self.BG,
        )

        self.style.configure(
            "Panel.TFrame",
            background=self.PANEL,
        )

        self.style.configure(
            "Header.TFrame",
            background=self.PANEL_2,
        )

        self.style.configure(
            "Card.TFrame",
            background=self.CARD,
        )

        self.style.configure(
            "Title.TLabel",
            background=self.PANEL_2,
            foreground=self.TEXT,
            font=("Segoe UI", 18, "bold"),
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=self.PANEL_2,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )

        self.style.configure(
            "PanelTitle.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("Segoe UI", 12, "bold"),
        )

        self.style.configure(
            "Field.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )

        self.style.configure(
            "Body.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Segoe UI", 10),
        )

        self.style.configure(
            "Result.TLabel",
            background=self.CARD,
            foreground=self.SUCCESS,
            font=("Segoe UI", 20, "bold"),
        )

        self.style.configure(
            "ResultCaption.TLabel",
            background=self.CARD,
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )

        self.style.configure(
            "Accent.TButton",
            background=self.ACCENT_2,
            foreground="#FFFFFF",
            borderwidth=0,
            padding=(16, 10),
            font=("Segoe UI", 9, "bold"),
        )

        self.style.map(
            "Accent.TButton",
            background=[
                ("active", self.ACCENT),
                ("pressed", "#0284C7"),
            ],
        )

        self.style.configure(
            "Secondary.TButton",
            background=self.CARD,
            foreground=self.TEXT,
            borderwidth=1,
            padding=(14, 10),
            font=("Segoe UI", 9),
        )

        self.style.map(
            "Secondary.TButton",
            background=[("active", self.BORDER)],
        )

        self.style.configure(
            "Modern.TCombobox",
            fieldbackground=self.CARD,
            background=self.CARD,
            foreground=self.TEXT,
            arrowcolor=self.ACCENT,
            bordercolor=self.BORDER,
            padding=6,
        )

        self.style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", self.CARD)],
            foreground=[("readonly", self.TEXT)],
        )

        self.root.option_add(
            "*TCombobox*Listbox.background",
            self.CARD,
        )
        self.root.option_add(
            "*TCombobox*Listbox.foreground",
            self.TEXT,
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectBackground",
            self.ACCENT_2,
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectForeground",
            "#FFFFFF",
        )

    # ========================================================
    # ІНТЕРФЕЙС
    # ========================================================

    def build_interface(self):
        main = ttk.Frame(
            self.root,
            style="App.TFrame",
        )
        main.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(
            main,
            style="Header.TFrame",
            padding=(24, 15),
        )
        header.pack(fill=tk.X)

        ttk.Label(
            header,
            text="FLIGHT PRICE PREDICTION",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Regression Models • Laboratory Work №3",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        workspace = ttk.Frame(
            main,
            style="App.TFrame",
            padding=18,
        )
        workspace.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(
            workspace,
            style="Panel.TFrame",
            padding=24,
        )
        left.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=(0, 14),
        )

        right = ttk.Frame(
            workspace,
            style="Panel.TFrame",
            width=470,
            padding=20,
        )
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)

        self.build_input_panel(left)
        self.build_result_panel(right)

    def build_input_panel(self, parent):
        ttk.Label(
            parent,
            text="ПАРАМЕТРИ РЕЙСУ",
            style="PanelTitle.TLabel",
        ).pack(anchor="w", pady=(0, 20))

        form = ttk.Frame(
            parent,
            style="Panel.TFrame",
        )
        form.pack(fill=tk.X)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        categories = self.metadata["categories"]
        self.input_vars = {}

        fields = [
            ("airline", "Авіакомпанія"),
            ("source_city", "Місто відправлення"),
            ("departure_time", "Час відправлення"),
            ("stops", "Кількість пересадок"),
            ("arrival_time", "Час прибуття"),
            ("destination_city", "Місто призначення"),
            ("class", "Клас квитка"),
        ]

        for index, (column, label) in enumerate(fields):
            row = index // 2
            col = index % 2

            field_frame = ttk.Frame(
                form,
                style="Panel.TFrame",
            )
            field_frame.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=(0, 18) if col == 0 else (0, 0),
                pady=(0, 15),
            )

            ttk.Label(
                field_frame,
                text=label + ":",
                style="Field.TLabel",
            ).pack(anchor="w")

            values = categories.get(column, [])
            default = values[0] if values else ""

            variable = tk.StringVar(value=default)
            self.input_vars[column] = variable

            combo = ttk.Combobox(
                field_frame,
                textvariable=variable,
                values=values,
                state="readonly",
                style="Modern.TCombobox",
            )
            combo.pack(fill=tk.X, pady=(6, 0))

        numeric_frame = ttk.Frame(
            form,
            style="Panel.TFrame",
        )
        numeric_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(4, 18),
        )

        numeric_frame.columnconfigure(0, weight=1)
        numeric_frame.columnconfigure(1, weight=1)

        self.duration_var = tk.StringVar(value="5.5")
        self.days_left_var = tk.StringVar(value="10")

        duration_frame = ttk.Frame(
            numeric_frame,
            style="Panel.TFrame",
        )
        duration_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 18),
        )

        ttk.Label(
            duration_frame,
            text="Тривалість польоту, год:",
            style="Field.TLabel",
        ).pack(anchor="w")

        tk.Entry(
            duration_frame,
            textvariable=self.duration_var,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 10),
        ).pack(
            fill=tk.X,
            ipady=8,
            pady=(6, 0),
        )

        days_frame = ttk.Frame(
            numeric_frame,
            style="Panel.TFrame",
        )
        days_frame.grid(
            row=0,
            column=1,
            sticky="ew",
        )

        ttk.Label(
            days_frame,
            text="Днів до вильоту:",
            style="Field.TLabel",
        ).pack(anchor="w")

        tk.Entry(
            days_frame,
            textvariable=self.days_left_var,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 10),
        ).pack(
            fill=tk.X,
            ipady=8,
            pady=(6, 0),
        )

        ttk.Label(
            parent,
            text="МОДЕЛЬ ДЛЯ ПРОГНОЗУ",
            style="PanelTitle.TLabel",
        ).pack(anchor="w", pady=(8, 12))

        self.model_var = tk.StringVar(
            value=self.model_names[0]
        )

        ttk.Combobox(
            parent,
            textvariable=self.model_var,
            values=self.model_names,
            state="readonly",
            width=38,
            style="Modern.TCombobox",
        ).pack(anchor="w", pady=(0, 18))

        buttons = ttk.Frame(
            parent,
            style="Panel.TFrame",
        )
        buttons.pack(anchor="w", pady=(0, 18))

        ttk.Button(
            buttons,
            text="Спрогнозувати вартість",
            style="Accent.TButton",
            command=self.predict_price,
        ).pack(side=tk.LEFT, padx=(0, 12))

        ttk.Button(
            buttons,
            text="Результати моделей",
            style="Secondary.TButton",
            command=self.show_model_results,
        ).pack(side=tk.LEFT, padx=(0, 12))

        ttk.Button(
            buttons,
            text="Очистити",
            style="Secondary.TButton",
            command=self.clear_output,
        ).pack(side=tk.LEFT)

        self.status_label = ttk.Label(
            parent,
            text="Готово до прогнозування. Повторне навчання не потрібне.",
            style="Body.TLabel",
        )
        self.status_label.pack(anchor="w", pady=(20, 0))

    def build_result_panel(self, parent):
        ttk.Label(
            parent,
            text="ІНФОРМАЦІЯ",
            style="PanelTitle.TLabel",
        ).pack(anchor="w", pady=(0, 15))

        price_card = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=18,
        )
        price_card.pack(fill=tk.X, pady=(0, 14))

        ttk.Label(
            price_card,
            text="ПРОГНОЗОВАНА ВАРТІСТЬ",
            style="ResultCaption.TLabel",
        ).pack(anchor="w")

        self.price_label = ttk.Label(
            price_card,
            text="—",
            style="Result.TLabel",
        )
        self.price_label.pack(anchor="w", pady=(8, 0))

        self.model_used_label = ttk.Label(
            price_card,
            text="",
            style="ResultCaption.TLabel",
        )
        self.model_used_label.pack(anchor="w", pady=(6, 0))

        self.info_text = tk.Text(
            parent,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            selectbackground=self.ACCENT_2,
            selectforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=14,
            pady=14,
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)

        self.info_text.tag_configure(
            "title",
            foreground=self.ACCENT,
            font=("Segoe UI", 11, "bold"),
        )

        self.info_text.tag_configure(
            "normal",
            foreground=self.TEXT,
            font=("Segoe UI", 10),
        )

        self.info_text.tag_configure(
            "muted",
            foreground=self.MUTED,
            font=("Segoe UI", 9),
        )

    # ========================================================
    # ЗБІР ТА ПЕРЕВІРКА ВХІДНИХ ДАНИХ
    # ========================================================

    def collect_input(self):
        try:
            duration = float(
                self.duration_var.get().strip().replace(",", ".")
            )
        except ValueError:
            raise ValueError(
                "Тривалість польоту повинна бути числом."
            )

        try:
            days_left = int(
                self.days_left_var.get().strip()
            )
        except ValueError:
            raise ValueError(
                "Кількість днів до вильоту повинна бути цілим числом."
            )

        if duration <= 0:
            raise ValueError(
                "Тривалість польоту повинна бути більшою за 0."
            )

        if days_left < 0:
            raise ValueError(
                "Кількість днів до вильоту не може бути від'ємною."
            )

        source_city = self.input_vars["source_city"].get()
        destination_city = self.input_vars["destination_city"].get()

        if source_city == destination_city:
            raise ValueError(
                "Місто відправлення та місто призначення "
                "не повинні співпадати."
            )

        warnings = []
        ranges = self.metadata.get("numeric_ranges", {})

        duration_range = ranges.get("duration")
        if duration_range:
            if not (
                duration_range["min"]
                <= duration
                <= duration_range["max"]
            ):
                warnings.append(
                    "Тривалість польоту виходить за межі "
                    "навчального датасету."
                )

        days_range = ranges.get("days_left")
        if days_range:
            if not (
                days_range["min"]
                <= days_left
                <= days_range["max"]
            ):
                warnings.append(
                    "Кількість днів до вильоту виходить за межі "
                    "навчального датасету."
                )

        row = {
            "airline": self.input_vars["airline"].get(),
            "source_city": source_city,
            "departure_time": self.input_vars["departure_time"].get(),
            "stops": self.input_vars["stops"].get(),
            "arrival_time": self.input_vars["arrival_time"].get(),
            "destination_city": destination_city,
            "class": self.input_vars["class"].get(),
            "duration": duration,
            "days_left": days_left,
        }

        return pd.DataFrame([row]), warnings

    # ========================================================
    # ПРОГНОЗ
    # ========================================================

    def predict_price(self):
        try:
            model_name = self.model_var.get()
            input_df, warnings = self.collect_input()

            self.status_label.config(
                text=f"Виконується прогноз: {model_name}..."
            )
            self.root.update_idletasks()

            model = self.get_model(model_name)

            prediction = float(
                model.predict(input_df)[0]
            )

            self.price_label.config(
                text=f"₹ {prediction:,.2f}"
            )

            self.model_used_label.config(
                text=f"Модель: {model_name}"
            )

            self.show_prediction_details(
                input_df.iloc[0].to_dict(),
                model_name,
                prediction,
                warnings,
            )

            self.status_label.config(
                text="Прогноз успішно отримано."
            )

        except Exception as error:
            self.status_label.config(
                text="Не вдалося виконати прогноз."
            )

            messagebox.showerror(
                "Помилка",
                str(error),
            )

    def show_prediction_details(
        self,
        row,
        model_name,
        prediction,
        warnings,
    ):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)

        self.info_text.insert(
            tk.END,
            "ВХІДНІ ДАНІ\n\n",
            "title",
        )

        labels = {
            "airline": "Авіакомпанія",
            "source_city": "Відправлення",
            "departure_time": "Час відправлення",
            "stops": "Пересадки",
            "arrival_time": "Час прибуття",
            "destination_city": "Призначення",
            "class": "Клас",
            "duration": "Тривалість",
            "days_left": "Днів до вильоту",
        }

        for key, value in row.items():
            text = f"{labels[key]}: {value}"

            if key == "duration":
                text += " год"

            self.info_text.insert(
                tk.END,
                text + "\n",
                "normal",
            )

        self.info_text.insert(
            tk.END,
            "\nРЕЗУЛЬТАТ\n\n",
            "title",
        )

        self.info_text.insert(
            tk.END,
            f"Обрана модель: {model_name}\n"
            f"Прогнозована вартість: ₹ {prediction:,.2f}\n",
            "normal",
        )

        metric_row = self.get_metric_row(model_name)

        if metric_row is not None:
            self.info_text.insert(
                tk.END,
                "\nЯКІСТЬ МОДЕЛІ НА VALIDATION\n\n",
                "title",
            )

            self.info_text.insert(
                tk.END,
                f"MAE:  {metric_row['MAE']:.2f}\n"
                f"RMSE: {metric_row['RMSE']:.2f}\n"
                f"R²:   {metric_row['R2']:.4f}\n",
                "normal",
            )

        if warnings:
            self.info_text.insert(
                tk.END,
                "\nУВАГА\n\n",
                "title",
            )

            for warning in warnings:
                self.info_text.insert(
                    tk.END,
                    "• " + warning + "\n",
                    "muted",
                )

        self.info_text.config(state=tk.DISABLED)

    # ========================================================
    # РЕЗУЛЬТАТИ НАВЧАННЯ
    # ========================================================

    def get_metric_row(self, model_name):
        if self.results_df.empty:
            return None

        rows = self.results_df[
            self.results_df["Model"] == model_name
        ]

        if rows.empty:
            return None

        return rows.iloc[0]

    def show_model_results(self):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)

        self.info_text.insert(
            tk.END,
            "РЕЗУЛЬТАТИ МОДЕЛЕЙ\n\n",
            "title",
        )

        if self.results_df.empty:
            self.info_text.insert(
                tk.END,
                "Файл model_results.csv не знайдено.\n"
                "Запустіть train_models.py.",
                "normal",
            )
            self.info_text.config(state=tk.DISABLED)
            return

        for _, row in self.results_df.iterrows():
            self.info_text.insert(
                tk.END,
                f"{row['Model']}\n",
                "title",
            )

            self.info_text.insert(
                tk.END,
                f"Час навчання: "
                f"{row['Training Time (s)']:.3f} с\n"
                f"Час прогнозу: "
                f"{row['Prediction Time (s)']:.3f} с\n"
                f"MAE:  {row['MAE']:.2f}\n"
                f"RMSE: {row['RMSE']:.2f}\n"
                f"R²:   {row['R2']:.4f}\n\n",
                "normal",
            )

        self.info_text.insert(
            tk.END,
            "Менші MAE та RMSE означають кращий результат, "
            "а R² бажано мати якомога ближчим до 1.",
            "muted",
        )

        self.info_text.config(state=tk.DISABLED)

        self.status_label.config(
            text="Показано результати навчання та validation-оцінювання."
        )

    # ========================================================
    # ОЧИЩЕННЯ
    # ========================================================

    def clear_output(self):
        self.price_label.config(text="—")
        self.model_used_label.config(text="")

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.config(state=tk.DISABLED)

        self.status_label.config(
            text="Готово до прогнозування. Повторне навчання не потрібне."
        )


def main():
    root = tk.Tk()

    try:
        FlightPriceApp(root)
    except SystemExit:
        root.destroy()
        return

    root.mainloop()


if __name__ == "__main__":
    main()
