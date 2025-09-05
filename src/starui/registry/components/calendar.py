from datetime import datetime, timedelta
from typing import Any, Literal
from uuid import uuid4

from starhtml import Div, Icon, Style
from starhtml.datastar import ds_effect, ds_on_click, ds_signals, ds_text, value

from .button import Button
from .utils import cn

CalendarMode = Literal["single", "range", "multiple"]


def Calendar(
    *,
    signal: str | None = None,
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    month: int | None = None,
    year: int | None = None,
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> Div:
    signal = signal or f"calendar_{uuid4().hex[:8]}"
    today = datetime.now()
    current_month = month or today.month
    current_year = year or today.year
    today_str = today.strftime("%Y-%m-%d")

    initial_selected = (
        selected
        if isinstance(selected, list) and mode in ("multiple", "range")
        else selected
        if isinstance(selected, str) and mode == "single"
        else []
        if mode in ("multiple", "range")
        else ""
    )

    calendar_data = _generate_calendar_data(current_month, current_year)
    month_display = _format_month_year(current_month, current_year)

    signals = {
        f"{signal}_month": value(current_month),
        f"{signal}_year": value(current_year),
        f"{signal}_selected": value(initial_selected),
        f"{signal}_calendar_data": value(calendar_data),
        f"{signal}_month_display": value(month_display),
    }

    return Div(
        Style(_CALENDAR_STYLES),
        Div(
            Button(
                Icon("lucide:chevron-left", cls="h-4 w-4"),
                *([ds_on_click(_nav_handler(signal, False))] if not disabled else []),
                variant="outline",
                size="icon",
                disabled=disabled,
                cls="h-7 w-7",
            ),
            Div(
                ds_text(f"${signal}_month_display"),
                ds_effect(_month_display_effect(signal)),
                cls="text-sm font-medium",
            ),
            Button(
                Icon("lucide:chevron-right", cls="h-4 w-4"),
                *([ds_on_click(_nav_handler(signal, True))] if not disabled else []),
                variant="outline",
                size="icon",
                disabled=disabled,
                cls="h-7 w-7",
            ),
            cls="flex items-center justify-between mb-4",
        ),
        Div(
            Div(
                *[
                    Div(
                        day,
                        cls="h-9 w-9 text-[0.8rem] font-normal text-muted-foreground text-center",
                    )
                    for day in ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")
                ],
                cls="grid grid-cols-7 border-b border-input mb-1",
            ),
            Div(
                ds_effect(_render_effect(signal, mode, disabled, today_str)),
                ds_on_click(_select_handler(signal, mode)) if not disabled else None,
                cls="cal-body grid grid-cols-7 gap-0",
                data_calendar_body=signal,
            ),
            cls="w-full",
        ),
        ds_signals(**signals),
        data_calendar=signal,
        cls=cn("p-3 border border-input rounded-md w-fit", class_name, cls),
        **attrs,
    )


def _month_display_effect(signal: str) -> str:
    return f"const m=['January','February','March','April','May','June','July','August','September','October','November','December'];${signal}_month_display=m[parseInt(${signal}_month)-1]+' '+${signal}_year"


def _nav_handler(signal: str, is_next: bool) -> str:
    op = "+" if is_next else "-"
    return f"let m=parseInt(${signal}_month){op}1,y=parseInt(${signal}_year);if(m>12){{m=1;y++}}else if(m<1){{m=12;y--}}${signal}_month=m;${signal}_year=y;const f=new Date(y,m-1,1),d=new Date(y,m,0).getDate(),o=f.getDay(),a=[];for(let i=0;i<42;i++){{const n=i-o+1,v=i>=o&&n<=d;a.push({{day:v?n.toString():'',date:v?`${{y}}-${{m.toString().padStart(2,'0')}}-${{n.toString().padStart(2,'0')}}`:'',empty:!v}})}}${signal}_calendar_data=a"


def _select_handler(signal: str, mode: CalendarMode) -> str:
    base = f"const c=evt.target.closest('.cal-cell');if(!c||c.classList.contains('empty'))return;const d=c.dataset.date;if(!d)return;const s=${signal}_selected||{'[]' if mode != 'single' else '""'};"

    if mode == "single":
        return base + f"${signal}_selected=s===d?'':d"
    elif mode == "multiple":
        return (
            base
            + f"const i=s.indexOf(d);${signal}_selected=i>=0?s.filter((_,x)=>x!==i):[...s,d]"
        )
    else:
        return (
            base
            + f"if(s.length===0)${signal}_selected=[d];else if(s.length===1)${signal}_selected=s[0]===d?[d,d]:[s[0],d].sort();else{{const r=s[0]===s[1]?d===s[0]:d>=s[0]&&d<=s[1];${signal}_selected=r?[]:[d]}}"
        )


def _render_effect(
    signal: str, mode: CalendarMode, disabled: bool, today_str: str
) -> str:
    sel_check = {
        "single": "s===c.date",
        "multiple": "s.includes(c.date)",
        "range": "s.length===1?c.date===s[0]:s.length===2?c.date>=s[0]&&c.date<=s[1]:false",
    }[mode]

    range_logic = ""
    if mode == "range":
        range_logic = "if(m==='range'&&s.length===2&&!e){const[a,b]=s;if(c.date===a&&a!==b)l+=' range-start';else if(c.date===b&&a!==b)l+=' range-end';else if(c.date>a&&c.date<b){l+=' range-middle';if(y===0)l+=' range-week-start';if(y===6)l+=' range-week-end'}else if(a===b&&c.date===a)l+=' range-single'}"

    return f"const d=${signal}_calendar_data||[],s=${signal}_selected||{'[]' if mode != 'single' else '""'},b=document.querySelector('[data-calendar-body=\"{signal}\"]'),m='{mode}';if(!b)return;${signal}_selected;let h='';for(let w=0;w<6;w++){{for(let y=0;y<7;y++){{const i=w*7+y,c=d[i]||{{}},e=!c.date,t=c.date==='{today_str}',x={sel_check};let l='cal-cell h-9 w-9 text-center text-sm rounded-md transition-colors flex items-center justify-center';if(!e&&!{str(disabled).lower()})l+=' cursor-pointer';if(e)l+=' empty';if(t)l+=' today';if(!e&&x)l+=' selected';{range_logic}h+=`<div class=\"${{l}}\" data-date=\"${{c.date||''}}\">${{c.day||''}}</div>`}}}}b.innerHTML=h"


def _format_month_year(month: int, year: int) -> str:
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return f"{months[month - 1]} {year}"


def _generate_calendar_data(month: int, year: int) -> list[dict[str, Any]]:
    first_day = datetime(year, month, 1)
    next_month = (
        datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
    )
    days_in_month = (next_month - timedelta(days=1)).day
    start_offset = first_day.weekday() + 1
    start_offset = 0 if start_offset == 7 else start_offset

    return [
        {
            "day": str(i - start_offset + 1)
            if start_offset <= i < start_offset + days_in_month
            else "",
            "date": f"{year}-{month:02d}-{i - start_offset + 1:02d}"
            if start_offset <= i < start_offset + days_in_month
            else "",
            "empty": not (start_offset <= i < start_offset + days_in_month),
        }
        for i in range(42)
    ]


_CALENDAR_STYLES = """
.cal-cell:not(.empty):not(.selected):hover{background-color:hsl(210 40% 96.1%)}
.cal-cell.selected{background-color:hsl(222.2 47.4% 11.2%)!important;color:hsl(210 40% 98%)!important}
.cal-cell.today{font-weight:600;box-shadow:inset 0 0 0 1px hsl(var(--border))}
.cal-cell.disabled{opacity:0.5;cursor:not-allowed}
.cal-cell.range-start{border-top-right-radius:0!important;border-bottom-right-radius:0!important}
.cal-cell.range-middle{border-radius:0!important;background-color:hsl(210 40% 96.1%);color:hsl(222.2 47.4% 11.2%)}
.cal-cell.range-middle.selected{background-color:hsl(222.2 47.4% 11.2%);color:hsl(210 40% 98%)}
.cal-cell.range-end{border-top-left-radius:0!important;border-bottom-left-radius:0!important}
.cal-cell.range-week-start{border-top-left-radius:0.375rem!important;border-bottom-left-radius:0.375rem!important}
.cal-cell.range-week-end{border-top-right-radius:0.375rem!important;border-bottom-right-radius:0.375rem!important}
[data-theme="dark"] .cal-cell:not(.empty):not(.selected):hover{background-color:hsl(217.2 32.6% 17.5%)}
[data-theme="dark"] .cal-cell.selected{background-color:hsl(210 40% 98%)!important;color:hsl(222.2 47.4% 11.2%)!important}
[data-theme="dark"] .cal-cell.range-middle{background-color:hsl(217.2 32.6% 17.5%);color:hsl(210 40% 98%)}
[data-theme="dark"] .cal-cell.range-middle.selected{background-color:hsl(210 40% 98%);color:hsl(222.2 47.4% 11.2%)}
"""
