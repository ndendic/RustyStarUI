from rusty_tags import *
from starui.registry.components.utils import Icon
from starui.registry.components.button import Button
from functools import cached_property
from pydantic import BaseModel


def SidebarButton(
    label: str,
    on_click: str | None = None,
    icon: str | None = None,
    variant='ghost',
    size="sm",
    cls="w-full justify-start",
    **attrs
) -> HtmlString:
    return Li(
            A(Icon(icon) if icon else None, label, on_click=DS.get(on_click), variant=variant, size=size, cls=cls, **attrs),
        ).render()


class SidebarBtn(BaseModel):
    label: str
    on_click: str | None = None
    icon: str | None = None

    def __str__(self):
        return SidebarButton(
            self.label,
            self.on_click,
            self.icon,
            variant='ghost',
            size='sm',
            cls='w-full justify-start align-middle',
        )

class Sidebar():
    buttons: AttrDict
    components: AttrDict

    def __init__(self):
        self.buttons = AttrDict()
        self.components = AttrDict()
    
    @cached_property
    def all_buttons(self):
        return [btn for btn in self.buttons.values()]
    
    @cached_property
    def all_components(self):
        return [btn for btn in self.components.values()]

sidebar_buttons = Sidebar()
sidebar_buttons.buttons.home = SidebarBtn(label="Home", on_click="/", icon="lucide:home")
sidebar_buttons.components.buttons = SidebarBtn(label="Buttons", on_click="/cmds/component.buttons/general")
sidebar_buttons.components.badges = SidebarBtn(label="Badges", on_click="/cmds/component.badges/general")
sidebar_buttons.components.inputs = SidebarBtn(label="Inputs", on_click="/cmds/component.inputs/general")
sidebar_buttons.components.cards = SidebarBtn(label="Cards", on_click="/cmds/component.cards/general")
sidebar_buttons.components.alerts = SidebarBtn(label="Alerts", on_click="/cmds/component.alerts/general")
sidebar_buttons.components.dialogs = SidebarBtn(label="Dialogs", on_click="/cmds/component.dialogs/general")
sidebar_buttons.components.radios = SidebarBtn(label="Radios", on_click="/cmds/component.radios/general")
sidebar_buttons.components.tabs = SidebarBtn(label="Tabs", on_click="/cmds/component.tabs/general")
sidebar_buttons.components.breadcrumb = SidebarBtn(label="Breadcrumb", on_click="/cmds/component.breadcrumb/general")
sidebar_buttons.components.switches = SidebarBtn(label="Switches", on_click="/cmds/component.switches/general")
sidebar_buttons.components.textareas = SidebarBtn(label="Textareas", on_click="/cmds/component.textareas/general")
sidebar_buttons.components.selects = SidebarBtn(label="Selects", on_click="/cmds/component.selects/general")
sidebar_buttons.components.popovers = SidebarBtn(label="Popovers", on_click="/cmds/component.popovers/general")
sidebar_buttons.components.tables = SidebarBtn(label="Tables", on_click="/cmds/component.tables/general")


sidebar = Aside(
    Nav(
        Section(
            Div(
                H3('Getting started', id='group-label-content-1'),
                Ul(                    
                    *sidebar_buttons.all_buttons,                    
                    Li(
                        Details(
                            Summary(
                                Icon('lucide:component'),
                                'Components',
                                aria_controls='submenu-content-1-3-content'
                            ),
                            Ul(
                                *sidebar_buttons.all_components,
                                id='submenu-content-1-3-content'
                            ),
                            id='submenu-content-1-3'
                        )
                    )
                ),
                role='group',
                aria_labelledby='group-label-content-1'
            ),
            cls='scrollbar'
        ),
        aria_label='Sidebar navigation'
    ),
    data_side='left',
    aria_hidden='false',
    cls='sidebar'
)

navbar = Header(
    Div(
        Button(
            Svg(
                Rect(width='18', height='18', x='3', y='3', rx='2'),
                Path(d='M9 3v18'),
                xmlns='http://www.w3.org/2000/svg',
                width='24',
                height='24',
                viewbox='0 0 24 24',
                fill='none',
                stroke='currentColor',
                stroke_width='2',
                stroke_linecap='round',
                stroke_linejoin='round'
            ),
            type='button',
            onclick="document.dispatchEvent(new CustomEvent('basecoat:sidebar'))",
            aria_label='Toggle sidebar',
            data_tooltip='Toggle sidebar',
            data_side='bottom',
            data_align='start',
            cls='btn-sm-icon-ghost mr-auto size-7 -ml-1.5'
        ),
        Select(
            Option('Default', value=''),
            Option('Claude', value='claude'),
            Option('Vercel', value='vercel'),
            Option('Candyland', value='candy'),
            id='theme-select',
            cls='select h-8 leading-none'
        ),
        Script("(() => {\r\n      const themeSelect = document.getElementById('theme-select');\r\n      const storedTheme = localStorage.getItem('themeVariant');\r\n      if (themeSelect && storedTheme) themeSelect.value = storedTheme;\r\n      themeSelect.addEventListener('change', () => {\r\n        const newTheme = themeSelect.value;\r\n        document.documentElement.classList.forEach(c => {\r\n          if (c.startsWith('theme-')) document.documentElement.classList.remove(c);\r\n        });\r\n        if (newTheme) {\r\n          document.documentElement.classList.add(`theme-${newTheme}`);\r\n          localStorage.setItem('themeVariant', newTheme);\r\n        } else {\r\n          localStorage.removeItem('themeVariant');\r\n        }\r\n      });\r\n    })();"),
        Button(
            Span(
                Svg(
                    Circle(cx='12', cy='12', r='4'),
                    Path(d='M12 2v2'),
                    Path(d='M12 20v2'),
                    Path(d='m4.93 4.93 1.41 1.41'),
                    Path(d='m17.66 17.66 1.41 1.41'),
                    Path(d='M2 12h2'),
                    Path(d='M20 12h2'),
                    Path(d='m6.34 17.66-1.41 1.41'),
                    Path(d='m19.07 4.93-1.41 1.41'),
                    xmlns='http://www.w3.org/2000/svg',
                    width='24',
                    height='24',
                    viewbox='0 0 24 24',
                    fill='none',
                    stroke='currentColor',
                    stroke_width='2',
                    stroke_linecap='round',
                    stroke_linejoin='round'
                ),
                cls='hidden dark:block'
            ),
            Span(
                Svg(
                    Path(d='M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z'),
                    xmlns='http://www.w3.org/2000/svg',
                    width='24',
                    height='24',
                    viewbox='0 0 24 24',
                    fill='none',
                    stroke='currentColor',
                    stroke_width='2',
                    stroke_linecap='round',
                    stroke_linejoin='round'
                ),
                cls='block dark:hidden'
            ),
            type='button',
            aria_label='Toggle dark mode',
            data_tooltip='Toggle dark mode',
            data_side='bottom',
            onclick="document.dispatchEvent(new CustomEvent('basecoat:theme'))",
            cls='btn-icon-outline size-8'
        ),
        A(
            Svg(
                Path(d='M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4'),
                Path(d='M9 18c-4.51 2-5-2-7-2'),
                xmlns='http://www.w3.org/2000/svg',
                width='24',
                height='24',
                viewbox='0 0 24 24',
                fill='none',
                stroke='currentColor',
                stroke_width='2',
                stroke_linecap='round',
                stroke_linejoin='round'
            ),
            href='https://github.com/ndendic/RustyStarUI',
            target='_blank',
            rel='noopener noreferrer',
            data_tooltip='GitHub repository',
            data_side='bottom',
            data_align='end',
            cls='btn-icon size-8'
        ),
        cls='flex h-14 w-full items-center gap-2 px-4'
    ),
    cls='bg-background sticky inset-x-0 top-0 isolate flex shrink-0 items-center gap-2 border-b z-10'
)

toggle_sidebar = Button('Toggle sidebar', type='button', onclick="document.dispatchEvent(new CustomEvent('basecoat:sidebar'))")