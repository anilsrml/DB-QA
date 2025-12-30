"""CLI arayüzü"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import box
from .database.connection import DatabaseConnection
from .agent.core import QueryAgent
from .utils.formatters import format_table
from .utils.logger import logger
from .config import settings


console = Console()


def print_welcome():
    """Hoş geldin mesajı göster"""
    welcome_text = """
# 🤖 PostgreSQL Doğal Dil Sorgu Sistemi

Veritabanınıza Türkçe sorular sorabilirsiniz!

**Örnek Sorular:**
- Kaç müşterimiz var?
- En pahalı 5 ürünü göster
- Hangi şehirden en fazla sipariş geldi?
- İstanbul'dan kaç müşteri var?

**Komutlar:**
- `help` - Yardım göster
- `schema` - Veritabanı yapısını göster
- `stats` - İstatistikleri göster
- `examples` - Örnek sorular göster
- `exit` veya `quit` - Çıkış
"""
    console.print(Panel(Markdown(welcome_text), border_style="blue"))


def print_help():
    """Yardım mesajı göster"""
    help_text = """
# 📖 Yardım

## Kullanım
Doğal Türkçe ile sorularınızı yazın. Sistem otomatik olarak SQL oluşturacak ve çalıştıracaktır.

## Özel Komutlar
- `help` - Bu yardım mesajını göster
- `schema` - Veritabanı tablolarını ve kolonlarını göster
- `stats` - Veritabanı istatistiklerini göster
- `examples` - Örnek sorular listesi
- `clear` - Ekranı temizle
- `exit` veya `quit` - Programdan çık

## İpuçları
- Spesifik sorular sorun (örn: "müşteriler" yerine "kaç müşteri var")
- Sayısal sonuçlar için "kaç", "toplam", "ortalama" gibi kelimeler kullanın
- Sıralama için "en çok", "en az", "ilk 5" gibi ifadeler kullanın
"""
    console.print(Markdown(help_text))


def print_schema(agent: QueryAgent):
    """Veritabanı schema'sını göster"""
    try:
        schema = agent.get_schema_info()
        
        for table_name, table_info in schema.items():
            # Tablo başlığı
            table_header = f"📋 {table_name}"
            if table_info.get("comment"):
                table_header += f" - {table_info['comment']}"
            
            console.print(f"\n[bold cyan]{table_header}[/bold cyan]")
            console.print(f"Satır sayısı: {table_info.get('row_count', 0)}")
            
            # Kolonlar tablosu
            col_table = Table(show_header=True, box=box.SIMPLE)
            col_table.add_column("Kolon", style="green")
            col_table.add_column("Tip", style="yellow")
            col_table.add_column("Açıklama", style="white")
            
            for col in table_info.get("columns", []):
                col_name = col["name"]
                if col["name"] == table_info.get("primary_key"):
                    col_name += " 🔑"
                
                col_type = col["type"]
                if not col["nullable"]:
                    col_type += " (NOT NULL)"
                
                col_comment = col.get("comment", "")
                
                col_table.add_row(col_name, col_type, col_comment)
            
            console.print(col_table)
            
            # Foreign keys
            if table_info.get("foreign_keys"):
                console.print("\n[bold]İlişkiler:[/bold]")
                for fk in table_info["foreign_keys"]:
                    console.print(
                        f"  • {fk['column_name']} → "
                        f"{fk['foreign_table_name']}.{fk['foreign_column_name']}"
                    )
    
    except Exception as e:
        console.print(f"[red]Schema gösterilirken hata: {str(e)}[/red]")


def print_stats(agent: QueryAgent):
    """Veritabanı istatistiklerini göster"""
    try:
        stats = agent.get_statistics()
        
        console.print(f"\n[bold cyan]📊 Veritabanı İstatistikleri[/bold cyan]\n")
        console.print(f"Toplam tablo sayısı: {stats['table_count']}")
        
        # Tablo istatistikleri
        stats_table = Table(show_header=True, box=box.ROUNDED)
        stats_table.add_column("Tablo", style="cyan")
        stats_table.add_column("Satır Sayısı", style="green", justify="right")
        stats_table.add_column("Kolon Sayısı", style="yellow", justify="right")
        stats_table.add_column("İlişkiler", style="magenta", justify="center")
        
        for table_name, table_stats in stats["tables"].items():
            has_fk = "✓" if table_stats["has_foreign_keys"] else "-"
            stats_table.add_row(
                table_name,
                str(table_stats["row_count"]),
                str(table_stats["column_count"]),
                has_fk,
            )
        
        console.print(stats_table)
    
    except Exception as e:
        console.print(f"[red]İstatistikler gösterilirken hata: {str(e)}[/red]")


def print_examples(agent: QueryAgent):
    """Örnek sorular göster"""
    suggestions = agent.suggest_questions(count=10)
    
    console.print("\n[bold cyan]💡 Örnek Sorular[/bold cyan]\n")
    for i, suggestion in enumerate(suggestions, 1):
        console.print(f"{i}. {suggestion}")
    console.print()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """PostgreSQL Doğal Dil Sorgu Sistemi"""
    if ctx.invoked_subcommand is None:
        # Alt komut yoksa interactive mode başlat
        ctx.invoke(interactive)


@cli.command()
def interactive():
    """İnteraktif mod - Sürekli soru-cevap"""
    print_welcome()
    
    # Veritabanı bağlantısını test et
    try:
        db = DatabaseConnection()
        if not db.test_connection():
            console.print("[red]❌ Veritabanı bağlantısı başarısız![/red]")
            console.print("[yellow]Lütfen .env dosyanızı kontrol edin.[/yellow]")
            return
        
        console.print("[green]✓ Veritabanına bağlanıldı[/green]\n")
        
        # Agent'ı başlat
        agent = QueryAgent(db)
        
    except Exception as e:
        console.print(f"[red]❌ Başlatma hatası: {str(e)}[/red]")
        console.print("[yellow]Lütfen .env dosyanızı ve veritabanı ayarlarınızı kontrol edin.[/yellow]")
        return
    
    # Ana döngü
    while True:
        try:
            # Kullanıcıdan input al
            question = console.input("\n[bold blue]Soru:[/bold blue] ").strip()
            
            if not question:
                continue
            
            # Özel komutlar
            if question.lower() in ['exit', 'quit', 'çıkış']:
                console.print("[yellow]Görüşmek üzere! 👋[/yellow]")
                break
            
            elif question.lower() == 'help':
                print_help()
                continue
            
            elif question.lower() == 'schema':
                print_schema(agent)
                continue
            
            elif question.lower() == 'stats':
                print_stats(agent)
                continue
            
            elif question.lower() in ['examples', 'örnekler']:
                print_examples(agent)
                continue
            
            elif question.lower() == 'clear':
                console.clear()
                print_welcome()
                continue
            
            # Normal sorgu
            with console.status("[bold green]Düşünüyorum...", spinner="dots"):
                result = agent.query(question, explain_results=True)
            
            # Sonuçları göster
            if result["success"]:
                console.print("\n[bold green]✅ Başarılı![/bold green]")
                
                # SQL'i göster
                if result.get("sql"):
                    console.print(f"\n[dim]SQL:[/dim] [cyan]{result['sql']}[/cyan]")
                
                # Açıklama
                if result.get("explanation"):
                    console.print(f"\n{result['explanation']}")
                
                # Sonuçlar tablosu
                if result.get("results"):
                    console.print()
                    table = format_table(result["results"], title="Sonuçlar")
                    console.print(table)
                
                # Metadata
                if result.get("metadata"):
                    meta = result["metadata"]
                    console.print(
                        f"\n[dim]Güven: {meta.get('confidence', 0):.0%} | "
                        f"Satır: {meta.get('row_count', 0)}[/dim]"
                    )
            else:
                console.print("\n[bold red]❌ Hata![/bold red]")
                if result.get("explanation"):
                    console.print(f"\n{result['explanation']}")
                elif result.get("error"):
                    console.print(f"\n{result['error']}")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]İptal edildi.[/yellow]")
            continue
        
        except Exception as e:
            console.print(f"\n[red]Beklenmeyen hata: {str(e)}[/red]")
            logger.error("Interactive mode error", error=str(e))


@cli.command()
@click.argument('question')
@click.option('--raw', is_flag=True, help='Ham sonuçları göster')
@click.option('--no-explain', is_flag=True, help='Açıklama yapma')
def query(question: str, raw: bool, no_explain: bool):
    """Tek bir sorgu çalıştır"""
    try:
        # Bağlantı ve agent
        db = DatabaseConnection()
        agent = QueryAgent(db)
        
        # Sorguyu çalıştır
        result = agent.query(question, explain_results=not no_explain)
        
        if result["success"]:
            if raw:
                # Ham JSON çıktısı
                import json
                console.print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                # Formatlanmış çıktı
                if result.get("explanation"):
                    console.print(result["explanation"])
                
                if result.get("results"):
                    console.print()
                    table = format_table(result["results"])
                    console.print(table)
        else:
            console.print(f"[red]Hata: {result.get('error', 'Bilinmeyen hata')}[/red]")
            return 1
    
    except Exception as e:
        console.print(f"[red]Hata: {str(e)}[/red]")
        return 1
    
    return 0


@cli.command()
def test():
    """Bağlantıyı test et"""
    try:
        console.print("Veritabanı bağlantısı test ediliyor...")
        
        db = DatabaseConnection()
        if db.test_connection():
            console.print("[green]✓ Bağlantı başarılı![/green]")
            
            # Schema bilgisi
            agent = QueryAgent(db)
            stats = agent.get_statistics()
            console.print(f"\nToplam {stats['table_count']} tablo bulundu.")
        else:
            console.print("[red]✗ Bağlantı başarısız![/red]")
            return 1
    
    except Exception as e:
        console.print(f"[red]Hata: {str(e)}[/red]")
        return 1
    
    return 0


if __name__ == "__main__":
    cli()

