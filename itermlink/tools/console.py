#======================== Rich ========================#
#------------- Imports -------------#
import rich.theme
import rich.progress
import rich.console
import rich.prompt # override input with Prompt.ask
# Improved tracebacks
import rich.traceback; rich.traceback.install()
#------------- Settings -------------#
# Store colors as variables for use with library objects
cblue = '#0675BB'
cgreen = 'green'
# Custom theme
theme = rich.theme.Theme({
    # Syntax highlighting for numbers, light mint
    "repr.number": "#9DFBCC",
    #--- Colors ---#
    'blue': cblue,
    'green': cgreen,
    #--- Meaning ---#
    'success': cgreen,
    # Emphasis
    'emph': cblue,
    # Amaranth red
    'warning': '#E03E52',
    'failure': '#E03E52'
})
#--- Input and printing ---#
console = rich.console.Console(theme=theme)
# Override
print = console.print
input = console.input
# New prompts
ask = lambda text : rich.prompt.Prompt.ask(
    text, console=console
)
confirm = lambda text, default=True : rich.prompt.Confirm.ask(
    text, default=default, console=console
)
# Provide a rich status function for indeterminate progress
status = lambda text: console.status(
    text, spinner='dots', spinner_style=cblue
)
#--- Progress bar ---#
def Progress(label='Progress'):
    """ Overload constructor for generating progress bars. """
    return rich.progress.Progress(
        rich.progress.SpinnerColumn('dots', style=cblue),
        rich.progress.TextColumn(f'{label}:', style=cblue),
        rich.progress.BarColumn(complete_style=cgreen, finished_style=cblue),
        rich.progress.MofNCompleteColumn(),
        console=console
    )
#======================== End Rich ========================#