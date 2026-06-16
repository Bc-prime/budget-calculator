# 💼 Budget Calculator — Value-Based Pricing

> Desktop app built with Python + CustomTkinter to calculate project budgets for software automation, applying **Value-Based Pricing** and **AI time optimization**.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-7B5EA7?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 🚀 What it does

Most freelancers price their work based on hours spent. This tool flips that logic:

**You charge for the value you deliver — not the time you invest.**

The app calculates:
- ✅ **Suggested Price** — what to charge the client (based on traditional hours × value factor)
- 🔒 **Minimum Floor** — the absolute minimum to cover your fixed costs
- 🚀 **Real Gain/Hour** — your effective hourly rate thanks to AI efficiency

---

## 📐 Pricing Formula

```
Minimum Rate  = Fixed Costs / Working Hours per Month
Floor Price   = AI Hours × Minimum Rate
Suggested Price = Traditional Hours × Minimum Rate × Value Factor
Real Gain/hr  = Suggested Price / AI Hours
```

---

## 🖥️ Screenshot

> _Add a screenshot here once you run the app_
> `![App Screenshot](screenshot.png)`

---

## ⚙️ Installation

**Requirements:** Python 3.8+

```bash
# 1. Clone the repo
git clone https://github.com/Bc-prime/budget-calculator.git
cd budget-calculator

# 2. Install dependency
pip install customtkinter

# 3. Run
python budget_calculator.py
```

---

## 🎛️ How to Use

| Field | Description |
|---|---|
| Fixed Monthly Costs | Rent, subscriptions, tools (USD) |
| Working Hours/Month | Real hours available for projects |
| Estimated Hours (no AI) | Traditional project time estimate |
| Real Hours (with AI) | Actual time using AI tools |
| Value/Complexity Factor | Slider 1.0× (simple) → 2.5× (critical) |

---

## 💡 The Logic Behind It

When you use AI tools, you deliver the same (or better) result in a fraction of the time. Traditional pricing penalizes your efficiency — you work faster but earn less.

**Value-Based Pricing fixes this:** the client pays for the outcome, not your hours. Your AI efficiency becomes pure profit.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **CustomTkinter 5.2+** — modern dark/light mode UI framework

---

## 👨‍💻 Author

**Rodrigo Córdoba** — Python Developer & Automation Freelancer

- 🌐 [Portfolio](https://bc-prime.github.io)
- 💼 [LinkedIn](https://linkedin.com/in/cordobars)
- 🐙 [GitHub](https://github.com/Bc-prime)
