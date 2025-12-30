"""Sonuç formatlama araçları"""

from typing import List, Dict, Any
from rich.table import Table
from rich.console import Console


def format_table(data: List[Dict[str, Any]], title: str = "Sonuçlar") -> Table:
    """
    Veritabanı sonuçlarını Rich table formatında döndür
    
    Args:
        data: Veritabanı sorgu sonuçları (dict listesi)
        title: Tablo başlığı
    
    Returns:
        Rich Table nesnesi
    """
    if not data:
        table = Table(title=title, show_header=False)
        table.add_row("Sonuç bulunamadı")
        return table
    
    # Tablo oluştur
    table = Table(title=title, show_header=True, header_style="bold magenta")
    
    # Kolonları ekle
    columns = list(data[0].keys())
    for col in columns:
        table.add_column(col, style="cyan")
    
    # Satırları ekle
    for row in data:
        table.add_row(*[str(value) if value is not None else "NULL" for value in row.values()])
    
    return table


def format_results(data: List[Dict[str, Any]], query: str = "") -> str:
    """
    Veritabanı sonuçlarını metin formatında döndür
    
    Args:
        data: Veritabanı sorgu sonuçları
        query: Çalıştırılan SQL sorgusu (opsiyonel)
    
    Returns:
        Formatlanmış metin
    """
    if not data:
        return "Sonuç bulunamadı."
    
    result_text = f"Toplam {len(data)} sonuç bulundu.\n\n"
    
    if query:
        result_text += f"Çalıştırılan Sorgu:\n{query}\n\n"
    
    # İlk birkaç satırı göster
    max_display = min(10, len(data))
    for i, row in enumerate(data[:max_display], 1):
        result_text += f"{i}. {row}\n"
    
    if len(data) > max_display:
        result_text += f"\n... ve {len(data) - max_display} sonuç daha."
    
    return result_text


def print_table(data: List[Dict[str, Any]], title: str = "Sonuçlar"):
    """
    Veritabanı sonuçlarını konsola yazdır
    
    Args:
        data: Veritabanı sorgu sonuçları
        title: Tablo başlığı
    """
    console = Console()
    table = format_table(data, title)
    console.print(table)

