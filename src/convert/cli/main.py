"""Módulo principal da interface de linha de comando (CLI) do Convert+."""
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table

from convert.core.conversor import Conversor

# O app é o objeto principal do Typer — ele agrupa todos os comandos
app = typer.Typer(
    name="convert+",
    help="Converte arquivos de texto entre formatos: MD, TXT, PDF e mais.",
    add_completion=False,
)

# Console do Rich — para mensagens coloridas no terminal
console = Console()


@app.command()
def converter(
    entrada: str = typer.Argument(
        ...,  # ... significa obrigatório
        help="Caminho do arquivo a ser convertido",
    ),
    formato: str = typer.Option(
        ...,
        "--formato", "-f",
        help="Formato de saída: md, txt, pdf, html",
    ),
    saida: str = typer.Option(
        ".",
        "--saida", "-s",
        help="Diretório onde o arquivo convertido será salvo",
    ),
    force: bool = typer.Option(
        False,
        "--force-overwrite",
        help="Sobrescrever arquivo existente sem criar cópia",
    ),
) -> None:
    """
    Converte um arquivo único para o formato especificado.

    Exemplos de uso:
        convert+ converter nota.md --formato txt
        convert+ converter relatorio.txt --formato md --saida ./saida/
        convert+ converter doc.md --formato txt --force-overwrite
    """
    c = Conversor()

    # Configura barra de progresso com estimativa de tempo
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,  # some da tela quando termina
    ) as barra:

        tarefa = barra.add_task("Convertendo...", total=100)

        # Registra o observer: a cada notificação do Core, atualiza a barra
        c.registrar_progresso(
            lambda percentual: barra.update(tarefa, completed=percentual)
        )

        try:
            resultado = c.converter(
                arquivo_entrada=entrada,
                formato_saida=formato,
                diretorio_saida=saida,
            )

            console.print(
                f"\n[green]✅ Concluído![/green] "
                f"Arquivo salvo em: [bold]{resultado['arquivo_saida']}[/bold]"
            )

        except FileNotFoundError as e:
            console.print(f"\n[red]❌ Arquivo não encontrado:[/red] {e}")
            raise typer.Exit(2)

        except ValueError as e:
            console.print(f"\n[red]❌ Erro de validação:[/red] {e}")
            raise typer.Exit(2)

        except Exception as e:
            console.print(f"\n[red]❌ Erro inesperado:[/red] {e}")
            raise typer.Exit(3)


@app.command()
def lote(
    diretorio: str = typer.Argument(
        ...,
        help="Pasta com os arquivos a converter",
    ),
    formato: str = typer.Option(
        ...,
        "--formato", "-f",
        help="Formato de saída para todos os arquivos",
    ),
    saida: str = typer.Option(
        "./saida",
        "--saida", "-s",
        help="Diretório onde os arquivos convertidos serão salvos",
    ),
    sim: bool = typer.Option(
        False,
        "--yes", "-y",
        help="Confirmar sem prompt interativo",
    ),
) -> None:
    """
    Converte todos os arquivos suportados de uma pasta.

    Exemplos de uso:
        convert+ lote ./documentos --formato txt
        convert+ lote ./docs --formato md --saida ./saida --yes
    """
    pasta = Path(diretorio)

    if not pasta.exists():
        console.print(f"[red]❌ Pasta não encontrada:[/red] {diretorio}")
        raise typer.Exit(2)

    extensoes = {".txt", ".md", ".pdf", ".docx", ".epub"}
    arquivos = [
        str(f) for f in pasta.rglob("*")
        if f.suffix.lower() in extensoes
    ]

    if not arquivos:
        console.print("[yellow]⚠️  Nenhum arquivo compatível encontrado.[/yellow]")
        raise typer.Exit(0)

    console.print(f"[blue]📂 {len(arquivos)} arquivo(s) encontrado(s)[/blue]")

    if not sim:
        confirmar = typer.confirm(
            f"Converter {len(arquivos)} arquivo(s) para .{formato}?"
        )
        if not confirmar:
            console.print("Operação cancelada.")
            raise typer.Exit(0)

    c = Conversor()

    with Progress(console=console) as barra:
        tarefa = barra.add_task("Processando lote...", total=100)

        resultados = c.converter_lote(
            arquivos=arquivos,
            formato_saida=formato,
            diretorio_saida=saida,
            callback_progresso=lambda p: barra.update(tarefa, completed=p),
        )

    sucessos = sum(1 for r in resultados if r["sucesso"])
    falhas = len(resultados) - sucessos

    console.print(f"\n[green]✅ {sucessos} convertido(s)[/green]", end="")
    if falhas:
        console.print(f"  [red]❌ {falhas} com erro[/red]")
    else:
        console.print()


@app.command()
def formatos() -> None:
    """Lista todos os formatos de conversão suportados."""
    tabela = Table(title="Formatos suportados pelo Convert+")
    tabela.add_column("De", style="cyan", justify="center")
    tabela.add_column("Para", style="green", justify="center")
    tabela.add_column("Status", justify="center")

    pares = [
        (".txt", "md",  "✅ Disponível"),
        (".md",  "txt", "✅ Disponível"),
        (".md",  "pdf", "🚧 Em breve"),
        (".txt", "pdf", "🚧 Em breve"),
        (".pdf", "txt", "🚧 Em breve"),
    ]

    for entrada, saida, status in pares:
        tabela.add_row(entrada, f".{saida}", status)

    console.print(tabela)


def main():
    """Ponto de entrada da aplicação."""
    app()


if __name__ == "__main__":
    main()
