import tkinter as tk
from tkinter import ttk

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

INPUT_FACTS = [
    {"name": "course_year", "label": "Курс навчання", "type": "int",
     "min": 1, "max": 6, "default": 3},
    {"name": "english_level", "label": "Рівень англійської мови", "type": "enum",
     "values": ["A2", "B1", "B2", "C1", "C2"], "default": "B2"},
    {"name": "gpa_level", "label": "Середній бал", "type": "enum",
     "values": ["low", "average", "high"], "default": "average",
     "titles": {"low": "низький", "average": "середній", "high": "високий"}},
    {"name": "has_research_papers", "label": "Наукові публікації", "type": "bool",
     "default": False},
    {"name": "has_portfolio", "label": "Портфоліо практичних проєктів",
     "type": "bool", "default": False},
    {"name": "work_experience_months", "label": "Досвід роботи за фахом, місяців",
     "type": "int", "min": 0, "max": 120, "default": 0},
    {"name": "needs_full_funding", "label": "Потребує повного фінансування",
     "type": "bool", "default": True},
    {"name": "preferred_track", "label": "Бажаний напрям", "type": "enum",
     "values": ["academic", "industry"], "default": "academic",
     "titles": {"academic": "науковий", "industry": "індустріальний"}},
    {"name": "academic_debts", "label": "Академічна заборгованість",
     "type": "bool", "default": False},
]

INTERMEDIATE_FACTS = [
    {"name": "language_ok", "label": "Мовний рівень відповідає вимогам"},
    {"name": "academic_excellence", "label": "Наукова відзнака"},
    {"name": "practical_readiness", "label": "Практична готовність"},
    {"name": "scholarship_qualified", "label": "Право на грант"},
    {"name": "funding_ok", "label": "Питання фінансування вирішене"},
    {"name": "not_eligible", "label": "Базові критерії не виконано"},
]

GOAL_FACT = "recommendation"

DECISIONS = {
    "RESEARCH_INTERNSHIP": {
        "label": "Наукове стажування в дослідницькій лабораторії",
        "text": "Профіль підтверджує наукову складову та право на фінансування."},
    "CORPORATE_INTERNSHIP": {
        "label": "Міжнародне корпоративне стажування",
        "text": "Практична підготовка достатня для стажування в компанії."},
    "ERASMUS_EXCHANGE": {
        "label": "Програма академічного обміну Erasmus+",
        "text": "Успішність і мовний рівень достатні для семестру за кордоном."},
    "SUMMER_SCHOOL": {
        "label": "Міжнародна літня школа",
        "text": "Резервний варіант мобільності з мінімальними вимогами."},
    "LANGUAGE_COURSE_FIRST": {
        "label": "Спочатку мовна підготовка",
        "text": "Мовний рівень нижчий за мінімальні вимоги програм."},
    "CLOSE_DEBTS_FIRST": {
        "label": "Спочатку закрити академічну заборгованість",
        "text": "Заборгованість унеможливлює участь у конкурсі."},
    "POSTPONE_AND_IMPROVE": {
        "label": "Відкласти участь і доопрацювати профіль",
        "text": "Базові критерії участі поки що не виконано."},
}

RULES = [
    {"id": "R01", "priority": 95,
     "text": "Рівень англійської B2 і вище відповідає вимогам програм мобільності",
     "if": {"all": [("english_level", "in", ["B2", "C1", "C2"])]},
     "then": ("language_ok", True)},

    {"id": "R02", "priority": 94,
     "text": "Рівень англійської A2 або B1 порушує базові критерії участі",
     "if": {"any": [("english_level", "==", "A2"), ("english_level", "==", "B1")]},
     "then": ("not_eligible", True)},

    {"id": "R03", "priority": 93,
     "text": "Студент 1 курсу ще не має сформованого академічного профілю",
     "if": {"all": [("course_year", "==", 1)]},
     "then": ("not_eligible", True)},

    {"id": "R04", "priority": 92,
     "text": "Академічна заборгованість є формальним блокером участі",
     "if": {"all": [("academic_debts", "==", True)]},
     "then": ("not_eligible", True)},

    {"id": "R05", "priority": 88,
     "text": "Високий бал разом із науковими публікаціями дає наукову відзнаку",
     "if": {"all": [("gpa_level", "==", "high"),
                    ("has_research_papers", "==", True)]},
     "then": ("academic_excellence", True)},

    {"id": "R06", "priority": 87,
     "text": "Портфоліо разом із високим або середнім балом підтверджує "
             "практичну готовність",
     "if": {"all": [("has_portfolio", "==", True),
                    ("gpa_level", "in", ["high", "average"])]},
     "then": ("practical_readiness", True)},

    {"id": "R07", "priority": 86,
     "text": "Досвід роботи від 6 місяців компенсує відсутність портфоліо",
     "if": {"all": [("work_experience_months", ">=", 6),
                    ("NOT", ("has_portfolio", "==", True))]},
     "then": ("practical_readiness", True)},

    {"id": "R08", "priority": 75,
     "text": "Наукова відзнака разом із мовною відповідністю дає право на грант",
     "if": {"all": [("academic_excellence", "==", True),
                    ("language_ok", "==", True)]},
     "then": ("scholarship_qualified", True)},

    {"id": "R09", "priority": 74,
     "text": "Практична готовність разом із вільним володінням мовою (C1/C2) "
             "дає право на грант",
     "if": {"all": [("practical_readiness", "==", True),
                    ("english_level", "in", ["C1", "C2"])]},
     "then": ("scholarship_qualified", True)},

    {"id": "R10", "priority": 65,
     "text": "Питання фінансування вирішене, якщо є право на грант або студент "
             "не потребує повного фінансування",
     "if": {"any": [("scholarship_qualified", "==", True),
                    ("needs_full_funding", "==", False)]},
     "then": ("funding_ok", True)},

    {"id": "R11", "priority": 50,
     "text": "Заборгованість вимагає першочергового закриття",
     "if": {"all": [("not_eligible", "==", True), ("academic_debts", "==", True)]},
     "then": (GOAL_FACT, "CLOSE_DEBTS_FIRST")},

    {"id": "R12", "priority": 45,
     "text": "Недостатній мовний рівень вимагає мовної підготовки",
     "if": {"all": [("not_eligible", "==", True),
                    ("english_level", "in", ["A2", "B1"])]},
     "then": (GOAL_FACT, "LANGUAGE_COURSE_FIRST")},

    {"id": "R13", "priority": 40,
     "text": "Базові критерії не виконано: участь відкладається",
     "if": {"all": [("not_eligible", "==", True)]},
     "then": (GOAL_FACT, "POSTPONE_AND_IMPROVE")},

    {"id": "R14", "priority": 35,
     "text": "Наукова відзнака, фінансування та науковий напрям дають наукове "
             "стажування",
     "if": {"all": [("academic_excellence", "==", True),
                    ("funding_ok", "==", True),
                    ("preferred_track", "==", "academic")]},
     "then": (GOAL_FACT, "RESEARCH_INTERNSHIP")},

    {"id": "R15", "priority": 30,
     "text": "Практична готовність, фінансування та індустріальний напрям дають "
             "корпоративне стажування",
     "if": {"all": [("practical_readiness", "==", True),
                    ("funding_ok", "==", True),
                    ("preferred_track", "==", "industry")]},
     "then": (GOAL_FACT, "CORPORATE_INTERNSHIP")},

    {"id": "R16", "priority": 25,
     "text": "Високий бал, мовна відповідність і вирішене фінансування дають "
             "програму обміну",
     "if": {"all": [("funding_ok", "==", True), ("language_ok", "==", True),
                    ("gpa_level", "==", "high")]},
     "then": (GOAL_FACT, "ERASMUS_EXCHANGE")},

    {"id": "R17", "priority": 10,
     "text": "Резервна рекомендація для мовно відповідного студента",
     "if": {"all": [("language_ok", "==", True)]},
     "then": (GOAL_FACT, "SUMMER_SCHOOL")},
]

EXTRA_RULES = [
    {"id": "R18", "priority": 20,
     "text": "Право на грант за науковим напрямом дає програму обміну навіть "
             "без високого середнього балу",
     "if": {"all": [("scholarship_qualified", "==", True),
                    ("preferred_track", "==", "academic")]},
     "then": (GOAL_FACT, "ERASMUS_EXCHANGE")},

    {"id": "R19", "priority": 12,
     "text": "Досвід роботи від року з відповідним мовним рівнем дає "
             "корпоративне стажування замість літньої школи",
     "if": {"all": [("language_ok", "==", True),
                    ("work_experience_months", ">=", 12)]},
     "then": (GOAL_FACT, "CORPORATE_INTERNSHIP")},
]

TEST_SCENARIOS = [
    {"id": "T1", "kind": "типовий",
     "name": "Сильний науковий профіль",
     "facts": {"course_year": 3, "english_level": "B2", "gpa_level": "high",
               "has_research_papers": True, "has_portfolio": False,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "RESEARCH_INTERNSHIP"},

    {"id": "T2", "kind": "альтернативне рішення",
     "name": "Практичний профіль, індустріальний напрям",
     "facts": {"course_year": 4, "english_level": "C1", "gpa_level": "average",
               "has_research_papers": False, "has_portfolio": True,
               "work_experience_months": 12, "needs_full_funding": True,
               "preferred_track": "industry", "academic_debts": False},
     "expect": "CORPORATE_INTERNSHIP"},

    {"id": "T3", "kind": "неповний набір фактів",
     "name": "Задано 3 факти з 9",
     "facts": {"course_year": 2, "english_level": "B2",
               "work_experience_months": 18},
     "expect": "SUMMER_SCHOOL", "expect_extended": "CORPORATE_INTERNSHIP"},

    {"id": "T4", "kind": "конфлікт правил",
     "name": "Профіль задовольняє умови трьох правил рішення",
     "facts": {"course_year": 4, "english_level": "C1", "gpa_level": "high",
               "has_research_papers": True, "has_portfolio": True,
               "work_experience_months": 0, "needs_full_funding": False,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "RESEARCH_INTERNSHIP"},

    {"id": "T5", "kind": "багатокрокове виведення",
     "name": "Рішення через три проміжні висновки",
     "facts": {"course_year": 3, "english_level": "C1", "gpa_level": "high",
               "has_research_papers": False, "has_portfolio": True,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "ERASMUS_EXCHANGE"},

    {"id": "T6", "kind": "блокуюче рішення",
     "name": "Академічна заборгованість за сильного профілю",
     "facts": {"course_year": 3, "english_level": "B2", "gpa_level": "high",
               "has_research_papers": True, "has_portfolio": False,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": True},
     "expect": "CLOSE_DEBTS_FIRST"},

    {"id": "T7", "kind": "блокуюче рішення",
     "name": "Недостатній рівень англійської мови",
     "facts": {"course_year": 3, "english_level": "B1", "gpa_level": "average",
               "has_research_papers": False, "has_portfolio": False,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "LANGUAGE_COURSE_FIRST"},

    {"id": "T8", "kind": "блокуюче рішення",
     "name": "Перший курс навчання",
     "facts": {"course_year": 1, "english_level": "B2", "gpa_level": "average",
               "has_research_papers": False, "has_portfolio": False,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "POSTPONE_AND_IMPROVE"},

    {"id": "T9", "kind": "резервне рішення",
     "name": "Середній профіль без гранту та практики",
     "facts": {"course_year": 3, "english_level": "B2", "gpa_level": "average",
               "has_research_papers": False, "has_portfolio": False,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "SUMMER_SCHOOL"},

    {"id": "T10", "kind": "перевірка модифікації БЗ",
     "name": "Грант за науковим напрямом, середній бал",
     "facts": {"course_year": 4, "english_level": "C1", "gpa_level": "average",
               "has_research_papers": False, "has_portfolio": True,
               "work_experience_months": 0, "needs_full_funding": True,
               "preferred_track": "academic", "academic_debts": False},
     "expect": "SUMMER_SCHOOL", "expect_extended": "ERASMUS_EXCHANGE"},

]


def all_rules(extended=False):
    return RULES + EXTRA_RULES if extended else list(RULES)


def fact_spec(name):
    for spec in INPUT_FACTS:
        if spec["name"] == name:
            return spec
    for spec in INTERMEDIATE_FACTS:
        if spec["name"] == name:
            return spec
    return {"name": name, "label": name, "type": "any"}


def show_value(name, value):
    if isinstance(value, bool):
        return "так" if value else "ні"
    if name == GOAL_FACT and value in DECISIONS:
        return DECISIONS[value]["label"]
    titles = fact_spec(name).get("titles", {})
    return titles.get(value, str(value))

def check(condition, facts):
    if isinstance(condition, dict):
        if "all" in condition:
            return all(check(item, facts) for item in condition["all"])
        return any(check(item, facts) for item in condition["any"])

    if condition[0] == "NOT":
        return not check(condition[1], facts)

    name, operation, expected = condition
    if name not in facts:
        return False
    value = facts[name]
    if operation == "==":
        return value == expected
    if operation == "!=":
        return value != expected
    if operation == "in":
        return value in expected
    if operation == ">=":
        return isinstance(value, int) and value >= expected
    if operation == "<=":
        return isinstance(value, int) and value <= expected
    raise ValueError("Невідома операція: " + str(operation))


def premises(condition, facts):
    if isinstance(condition, dict):
        items = condition.get("all") or condition["any"]
        found = []
        for item in items:
            if "all" in condition or check(item, facts):
                found += premises(item, facts)
        return found
    if condition[0] == "NOT":
        return [(condition[1][0], facts.get(condition[1][0], "невідомо"))]
    return [(condition[0], facts.get(condition[0], "невідомо"))]


def condition_vars(condition):
    if isinstance(condition, dict):
        items = condition.get("all") or condition["any"]
        names = []
        for item in items:
            names += condition_vars(item)
        return names
    if condition[0] == "NOT":
        return condition_vars(condition[1])
    return [condition[0]]


def condition_text(condition):
    if isinstance(condition, dict):
        if "all" in condition:
            return " AND ".join(condition_text(c) for c in condition["all"])
        return " OR ".join(condition_text(c) for c in condition["any"])
    if condition[0] == "NOT":
        return "NOT " + condition_text(condition[1])
    name, operation, expected = condition
    if isinstance(expected, list):
        expected = "[" + ", ".join(str(v) for v in expected) + "]"
    return "%s %s %s" % (name, operation, expected)


def rule_text(rule):
    return "IF %s THEN %s = %s" % (condition_text(rule["if"]),
                                   rule["then"][0], rule["then"][1])


class Result:

    def __init__(self, initial):
        self.facts = dict(initial)
        self.source = {name: "вхідний факт" for name in initial}
        self.steps = []
        self.rejected = []
        self.cycles = 0

    @property
    def decision(self):
        return self.facts.get(GOAL_FACT)

    def fired_ids(self):
        return [step["rule"]["id"] for step in self.steps]


def infer(rules, initial_facts):
    result = Result(initial_facts)
    used = set()

    while True:
        result.cycles += 1
        conflict_set = [rule for rule in rules
                        if rule["id"] not in used and check(rule["if"], result.facts)]
        if not conflict_set:
            break

        rule = max(conflict_set, key=lambda item: item["priority"])
        conflict_set.sort(key=lambda item: -item["priority"])
        used.add(rule["id"])
        name, value = rule["then"]

        if name in result.facts:
            result.rejected.append({
                "rule": rule,
                "reason": "факт %s уже виведено правилом %s зі значенням %s"
                          % (name, result.source[name], result.facts[name])})
            continue

        support = premises(rule["if"], result.facts)
        result.facts[name] = value
        result.source[name] = rule["id"]
        result.steps.append({"rule": rule, "produced": (name, value),
                             "premises": support,
                             "conflict": [r["id"] for r in conflict_set]})
    return result

def explanation_text(result):
    lines = ["ПОЧАТКОВІ ФАКТИ:"]
    for name, value in result.facts.items():
        if result.source[name] == "вхідний факт":
            lines.append("   %s = %s" % (name, show_value(name, value)))

    lines.append("")
    lines.append("АКТИВОВАНІ ПРАВИЛА:")
    if not result.steps:
        lines.append("   жодне правило не спрацювало")
    for number, step in enumerate(result.steps, 1):
        rule = step["rule"]
        conflict = ""
        if len(step["conflict"]) > 1:
            conflict = "   конфліктна множина: %s" % ", ".join(step["conflict"])
        lines.append("")
        lines.append("   Крок %d. %s (пріоритет %d)%s"
                     % (number, rule["id"], rule["priority"], conflict))
        lines.append("      %s" % rule["text"])
        lines.append("      %s" % rule_text(rule))
        lines.append("      обґрунтування: " + ", ".join(
            "%s = %s" % (name, show_value(name, value))
            for name, value in step["premises"]))
        lines.append("      отримано факт: %s = %s"
                     % (step["produced"][0],
                        show_value(*step["produced"])))

    if result.rejected:
        lines.append("")
        lines.append("ВІДХИЛЕНІ ПРАВИЛА (розв'язання конфлікту за пріоритетом):")
        for item in result.rejected:
            lines.append("   %s (пріоритет %d) — %s"
                         % (item["rule"]["id"], item["rule"]["priority"],
                            item["reason"]))

    lines.append("")
    lines.append("РЕЗУЛЬТАТ: " + (
        "%s — %s" % (result.decision, DECISIONS[result.decision]["label"])
        if result.decision else "рішення не сформовано"))
    return "\n".join(lines)


def chain_text(result, name=None, level=0):
    name = name or GOAL_FACT
    if name not in result.facts:
        return "Цільовий факт не виведено."

    indent = "    " * level
    origin = result.source[name]
    lines = ["%s%s = %s" % (indent, name, show_value(name, result.facts[name]))]
    if origin == "вхідний факт":
        lines[0] += "   [початковий факт]"
        return "\n".join(lines)

    step = next(s for s in result.steps if s["produced"][0] == name)
    lines[0] += "   [правило %s: %s]" % (origin, step["rule"]["text"])
    for premise_name, _ in step["premises"]:
        lines.append(chain_text(result, premise_name, level + 1))
    return "\n".join(lines)

BG = "#0B1120"
PANEL = "#111827"
CARD = "#1E293B"
BORDER = "#334155"
TEXT = "#E5E7EB"
MUTED = "#94A3B8"
ACCENT = "#38BDF8"
GREEN = "#34D399"
RED = "#FB7185"
ORANGE = "#F97316"
NOT_SET = "— не задано —"


class Application:
    def __init__(self, root):
        self.root = root
        self.result = None
        self.fields = {}

        root.title("Система, заснована на знаннях - академічна мобільність")
        root.geometry("1360x860")
        root.minsize(1100, 700)
        root.configure(bg=BG)

        self.extended = tk.BooleanVar(value=False)
        self.scenario = tk.StringVar()
        self.status = tk.StringVar(value="Задайте початкові факти та натисніть "
                                         "«Виконати виведення».")
        self._styles()
        self._header()
        self._body()
        self._defaults()
        self._show_rules()
        self._draw_graph()

    # -- оформлення -------------------------------------------------------- #

    def _styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=PANEL)
        style.configure("Bg.TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)
        style.configure("Title.TLabel", background=PANEL, foreground=TEXT,
                        font=("Segoe UI", 15, "bold"))
        style.configure("Sub.TLabel", background=PANEL, foreground=MUTED,
                        font=("Segoe UI", 9))
        style.configure("Field.TLabel", background=PANEL, foreground=TEXT,
                        font=("Segoe UI", 9))
        style.configure("Decision.TLabel", background=CARD, foreground=GREEN,
                        font=("Segoe UI", 11, "bold"), wraplength=290,
                        justify="left")
        style.configure("Go.TButton", background="#0EA5E9", foreground="#FFFFFF",
                        borderwidth=0, padding=(12, 8),
                        font=("Segoe UI", 9, "bold"))
        style.map("Go.TButton", background=[("active", ACCENT)])
        style.configure("TCheckbutton", background=PANEL, foreground=TEXT,
                        font=("Segoe UI", 9))
        style.map("TCheckbutton", background=[("active", PANEL)])
        style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                        foreground=TEXT, arrowcolor=ACCENT, bordercolor=BORDER,
                        padding=4)
        style.map("TCombobox", fieldbackground=[("readonly", CARD)],
                  foreground=[("readonly", TEXT)],
                  selectbackground=[("readonly", CARD)],
                  selectforeground=[("readonly", TEXT)])
        style.configure("TSpinbox", fieldbackground=CARD, background=CARD,
                        foreground=TEXT, arrowcolor=ACCENT, padding=3)
        style.configure("TNotebook", background=PANEL, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL, foreground=MUTED,
                        padding=(14, 7), borderwidth=0, font=("Segoe UI", 9))
        style.map("TNotebook.Tab", background=[("selected", CARD)],
                  foreground=[("selected", ACCENT)])
        style.configure("Treeview", background=CARD, fieldbackground=CARD,
                        foreground=TEXT, borderwidth=0, rowheight=22,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=PANEL, foreground=MUTED,
                        relief="flat", font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#0EA5E9")],
                  foreground=[("selected", "#FFFFFF")])
        style.configure("TScrollbar", background=BORDER, troughcolor=PANEL,
                        bordercolor=PANEL, arrowcolor=MUTED)
        self.root.option_add("*TCombobox*Listbox.background", CARD)
        self.root.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#0EA5E9")

    def _header(self):
        head = ttk.Frame(self.root, padding=(16, 10))
        head.pack(fill="x")
        ttk.Label(head, text="Система підтримки прийняття рішень, "
                             "заснована на знаннях", style="Title.TLabel").pack(
            anchor="w")
        ttk.Label(head, text="Предметна область: міжнародна академічна "
                             "мобільність студентів. Продукційна база знань, "
                             "пряме логічне виведення (forward chaining).",
                  style="Sub.TLabel").pack(anchor="w")

    def _body(self):
        body = ttk.Frame(self.root, style="Bg.TFrame", padding=(12, 6, 12, 6))
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body, padding=(12, 12))
        left.pack(side="left", fill="y")
        self._input_panel(left)

        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))
        self._tabs(right)

        bar = ttk.Frame(self.root, padding=(16, 6))
        bar.pack(fill="x", side="bottom")
        ttk.Label(bar, textvariable=self.status, style="Sub.TLabel").pack(anchor="w")

    def _input_panel(self, parent):
        ttk.Label(parent, text="ПОЧАТКОВІ ФАКТИ", style="Title.TLabel").pack(
            anchor="w")
        ttk.Label(parent, text="Значення «— не задано —» лишає факт невідомим.",
                  style="Sub.TLabel").pack(anchor="w", pady=(0, 8))

        for spec in INPUT_FACTS:
            row = ttk.Frame(parent)
            row.pack(fill="x", pady=3)
            ttk.Label(row, text=spec["label"], style="Field.TLabel").pack(anchor="w")
            variable = tk.StringVar()
            if spec["type"] == "bool":
                widget = ttk.Combobox(row, textvariable=variable, state="readonly",
                                      width=30, values=[NOT_SET, "так", "ні"])
            elif spec["type"] == "enum":
                titles = spec.get("titles", {})
                values = [NOT_SET] + ["%s — %s" % (v, titles[v]) if v in titles
                                      else v for v in spec["values"]]
                widget = ttk.Combobox(row, textvariable=variable, state="readonly",
                                      width=30, values=values)
            else:
                widget = ttk.Spinbox(row, textvariable=variable, width=30,
                                     from_=spec["min"], to=spec["max"])
            widget.pack(fill="x")
            self.fields[spec["name"]] = variable

        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(parent, text="Готовий тестовий сценарій", style="Field.TLabel").pack(
            anchor="w")
        box = ttk.Combobox(parent, textvariable=self.scenario, state="readonly",
                           width=30,
                           values=["%s — %s" % (s["id"], s["name"])
                                   for s in TEST_SCENARIOS])
        box.pack(fill="x", pady=(2, 8))
        box.bind("<<ComboboxSelected>>", lambda event: self._load_scenario())

        ttk.Checkbutton(parent, text="Модифікована база знань (+2 правила)",
                        variable=self.extended,
                        command=self._switch_kb).pack(anchor="w", pady=(0, 8))

        ttk.Button(parent, text="Виконати виведення", style="Go.TButton",
                   command=self.run).pack(fill="x")
        ttk.Button(parent, text="Значення за замовчуванням",
                   command=self._defaults).pack(fill="x", pady=4)

        card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill="x", pady=(8, 0))
        tk.Label(card, text="РЕКОМЕНДАЦІЯ", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w", padx=10, pady=(8, 2))
        self.decision_label = ttk.Label(card, text="виведення не виконувалося",
                                        style="Decision.TLabel")
        self.decision_label.pack(anchor="w", padx=10, pady=(0, 10))

    def _tabs(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        self.chain_text = self._text_tab("Хід виведення та пояснення")
        self._graph_tab()
        self._rules_tab()

    def _text_tab(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        text = tk.Text(frame, wrap="none", font=("Consolas", 9), bg=CARD, fg=TEXT,
                       relief="flat", padx=10, pady=8, borderwidth=0)
        bar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=bar.set, state="disabled")
        text.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")
        return text

    def _rules_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="База знань")
        ttk.Label(frame, text="Після виведення: зелений — правило спрацювало, "
                              "червоний — відхилено під час розв'язання конфлікту.",
                  style="Sub.TLabel").pack(anchor="w", padx=8, pady=6)
        columns = ("priority", "rule", "meaning")
        self.rules_table = ttk.Treeview(frame, columns=columns, show="tree headings")
        self.rules_table.heading("#0", text="ID")
        self.rules_table.heading("priority", text="Пріоритет")
        self.rules_table.heading("rule", text="IF (умова) THEN (висновок)")
        self.rules_table.heading("meaning", text="Зміст правила")
        self.rules_table.column("#0", width=55)
        self.rules_table.column("priority", width=70, anchor="center")
        self.rules_table.column("rule", width=470)
        self.rules_table.column("meaning", width=380)
        bar = ttk.Scrollbar(frame, orient="vertical", command=self.rules_table.yview)
        self.rules_table.configure(yscrollcommand=bar.set)
        self.rules_table.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")
        self.rules_table.tag_configure("fired", background="#12312A", foreground=GREEN)
        self.rules_table.tag_configure("rejected", background="#3A1D24",
                                       foreground=RED)

    def _graph_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Структура бази знань")
        if not HAS_MATPLOTLIB:
            tk.Label(frame, text="Для графа потрібна бібліотека matplotlib.",
                     bg=PANEL, fg=MUTED).pack(expand=True)
            self.figure = None
            return
        self.figure = Figure(figsize=(10, 6.5), dpi=100, facecolor=PANEL)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # -- робота з формою --------------------------------------------------- #

    def _defaults(self):
        for spec in INPUT_FACTS:
            self._set_field(spec["name"], spec["default"])
        self.scenario.set("")

    def _set_field(self, name, value):
        spec = fact_spec(name)
        if value is None:
            self.fields[name].set("" if spec["type"] == "int" else NOT_SET)
        elif spec["type"] == "bool":
            self.fields[name].set("так" if value else "ні")
        elif spec["type"] == "enum":
            titles = spec.get("titles", {})
            self.fields[name].set("%s — %s" % (value, titles[value])
                                  if value in titles else str(value))
        else:
            self.fields[name].set(str(value))

    def _load_scenario(self):
        chosen = self.scenario.get().split(" — ")[0]
        scenario = next(s for s in TEST_SCENARIOS if s["id"] == chosen)
        for spec in INPUT_FACTS:
            self._set_field(spec["name"], scenario["facts"].get(spec["name"]))
        self.status.set("Завантажено сценарій %s (%s): %s"
                        % (scenario["id"], scenario["kind"], scenario["name"]))

    def _collect(self):
        """Читає початкові факти з форми."""
        facts = {}
        for spec in INPUT_FACTS:
            raw = self.fields[spec["name"]].get().strip()
            if raw in ("", NOT_SET):
                continue
            if spec["type"] == "bool":
                facts[spec["name"]] = raw == "так"
            elif spec["type"] == "enum":
                facts[spec["name"]] = raw.split(" — ")[0]
            else:
                try:
                    facts[spec["name"]] = int(raw)
                except ValueError:
                    self.status.set("Факт «%s»: потрібно ціле число."
                                    % spec["label"])
                    return None
        return facts

    def _switch_kb(self):
        self.result = None
        self._show_rules()
        self._draw_graph()
        self.status.set("Використовується %s база знань (%d правил)."
                        % ("модифікована" if self.extended.get() else "базова",
                           len(all_rules(self.extended.get()))))

    # -- запуск виведення -------------------------------------------------- #

    def run(self):
        facts = self._collect()
        if facts is None:
            return
        self.result = infer(all_rules(self.extended.get()), facts)

        self._set_text(self.chain_text,
                       "ЛАНЦЮЖОК ЛОГІЧНОГО ВИВЕДЕННЯ\n" + "=" * 60 + "\n"
                       + chain_text(self.result) + "\n\n"
                       + self._decision_block() + "\n\n"
                       + "ПРОТОКОЛ ВИВЕДЕННЯ\n" + "=" * 60 + "\n"
                       + explanation_text(self.result))
        self._show_rules()
        self._draw_graph()

        decision = self.result.decision
        self.decision_label.configure(
            text=DECISIONS[decision]["label"] if decision else "рішення не сформовано",
            foreground=GREEN if decision else RED)
        self.status.set("Виведення завершено за %d циклів; активовано правил: %s%s"
                        % (self.result.cycles,
                           ", ".join(self.result.fired_ids()) or "жодного",
                           self._expected_note(facts)))
        self.notebook.select(0)

    def _expected_note(self, facts):
        for scenario in TEST_SCENARIOS:
            if scenario["facts"] != facts:
                continue
            key = ("expect_extended" if self.extended.get()
                   and "expect_extended" in scenario else "expect")
            expected = scenario[key]
            return ("   |   сценарій %s: очікувано %s — %s"
                    % (scenario["id"], expected,
                       "результат правильний" if self.result.decision == expected
                       else "РОЗБІЖНІСТЬ"))
        return ""

    def _decision_block(self):
        decision = self.result.decision
        if not decision:
            return ("РІШЕННЯ НЕ СФОРМОВАНО\nЖодне правило формування рішення "
                    "не застосовне до заданого набору фактів.")
        info = DECISIONS[decision]
        return ("РЕКОМЕНДАЦІЯ\n" + "=" * 60
                + "\n%s\n%s\nКод рішення: %s\nСформовано правилом: %s"
                % (info["label"], info["text"], decision,
                   self.result.source[GOAL_FACT]))

    # -- оновлення вкладок ------------------------------------------------- #

    def _set_text(self, widget, content):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content)
        widget.configure(state="disabled")

    def _show_rules(self):
        self.rules_table.delete(*self.rules_table.get_children())
        fired = set(self.result.fired_ids()) if self.result else set()
        rejected = ({item["rule"]["id"] for item in self.result.rejected}
                    if self.result else set())
        for rule in all_rules(self.extended.get()):
            tag = "fired" if rule["id"] in fired else (
                "rejected" if rule["id"] in rejected else "")
            self.rules_table.insert("", "end", text=rule["id"],
                                    values=(rule["priority"], rule_text(rule),
                                            rule["text"]),
                                    tags=(tag,) if tag else ())

    # -- граф структури бази знань ----------------------------------------- #

    def _draw_graph(self):
        if not HAS_MATPLOTLIB:
            return
        rules = all_rules(self.extended.get())
        axes = self.axes
        axes.clear()
        axes.set_facecolor(BG)
        axes.set_xticks([])
        axes.set_yticks([])
        for spine in axes.spines.values():
            spine.set_visible(False)

        # стовпці: вхідні факти -> проміжні факти (за рівнем) -> рішення
        column = {spec["name"]: 0 for spec in INPUT_FACTS}
        for _ in range(len(INTERMEDIATE_FACTS)):
            for rule in rules:
                target = rule["then"][0]
                if target == GOAL_FACT:
                    continue
                sources = condition_vars(rule["if"])
                if all(name in column for name in sources):
                    column[target] = max(column[target] if target in column else 0,
                                         max(column[name] for name in sources) + 1)
        last = max(column.values()) + 1
        for code in DECISIONS:
            column[code] = last

        groups = {}
        for name, index in column.items():
            groups.setdefault(index, []).append(name)
        position = {}
        height = max(len(names) for names in groups.values())
        for index, names in groups.items():
            for order, name in enumerate(names):
                shift = (height - len(names)) / 2.0
                position[name] = (index * 3.4, -(order + shift) * 1.15)

        fired = set(self.result.fired_ids()) if self.result else set()
        for rule in rules:
            target = rule["then"][0]
            target = rule["then"][1] if target == GOAL_FACT else target
            active = rule["id"] in fired
            for name in set(condition_vars(rule["if"])):
                if name not in position or target not in position:
                    continue
                x1, y1 = position[name]
                x2, y2 = position[target]
                axes.annotate("", xy=(x2 - 0.95, y2), xytext=(x1 + 0.95, y1),
                              arrowprops=dict(arrowstyle="-|>",
                                              color=ACCENT if active else BORDER,
                                              linewidth=1.6 if active else 0.7,
                                              alpha=1.0 if active else 0.55))
            if active:
                x1, y1 = position[condition_vars(rule["if"])[0]]
                x2, y2 = position[target]
                axes.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.1, rule["id"],
                          color=ACCENT, fontsize=7, ha="center")

        derived = self.result.facts if self.result else {}
        for name, (x, y) in position.items():
            if name in DECISIONS:
                face, line = "#33271A", ORANGE
                if derived.get(GOAL_FACT) == name:      # сформоване рішення
                    face, line = "#4A3517", GREEN
            elif any(spec["name"] == name for spec in INPUT_FACTS):
                face, line = "#1B2438", "#7DD3FC"
            else:
                face, line = ("#12312A", GREEN) if name in derived else (CARD, BORDER)
            axes.text(x, y, name, ha="center", va="center", fontsize=7.5, color=TEXT,
                      bbox=dict(boxstyle="round,pad=0.35", facecolor=face,
                                edgecolor=line, linewidth=1.2))

        axes.set_xlim(-1.6, last * 3.4 + 1.9)
        ys = [point[1] for point in position.values()]
        axes.set_ylim(min(ys) - 1.0, max(ys) + 1.0)
        axes.set_title("Структура бази знань: початкові факти -> проміжні "
                       "висновки -> кінцеві рішення\n"
                       "(блакитним виділено правила, що спрацювали)",
                       color=TEXT, fontsize=10, pad=10)
        self.figure.tight_layout()
        self.canvas.draw_idle()


def main():
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
