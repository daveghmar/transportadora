$files = Get-ChildItem -Filter *.html | Where-Object { $_.Name -ne 'index.html' }
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match "if \s*\(\s*([a-zA-Z0-9_]+)\.length\s*===\s*0\s*\)") {
        $arrName = $matches[1]
        
        $newFunc = @"
  function exportarExcel() {
    if ($arrName.length === 0) {
      alert('Nenhum código para exportar.');
      return;
    }
    
    const marcaNome = document.querySelector('h2').innerText.trim();
    let esperado = 0;
    try {
        const esperadoPorMarca = JSON.parse(localStorage.getItem('esperado_por_marca') || '{}');
        esperado = esperadoPorMarca[marcaNome] || 0;
    } catch(e) {}

    const wb = XLSX.utils.book_new();

    // Planilha de Resumo
    const resumoDados = [
        { 'Marca': marcaNome, 'Esperado': esperado, 'Lido': $arrName.length, 'Faltam': esperado - $arrName.length }
    ];
    const wsResumo = XLSX.utils.json_to_sheet(resumoDados);
    wsResumo['!cols'] = [ { wch: 20 }, { wch: 15 }, { wch: 15 }, { wch: 15 } ];
    XLSX.utils.book_append_sheet(wb, wsResumo, 'Resumo');

    // Planilha de Detalhes
    const detalhesDados = $arrName.map((c, i) => ({ 'Ordem': i + 1, 'Código de Barras': c.codigo, 'Hora da Leitura': c.hora }));
    const wsDetalhes = XLSX.utils.json_to_sheet(detalhesDados);
    wsDetalhes['!cols'] = [ { wch: 10 }, { wch: 40 }, { wch: 20 } ];
    XLSX.utils.book_append_sheet(wb, wsDetalhes, 'Detalhes');

    const dataFormatada = new Date().toLocaleDateString('pt-BR').replace(/\//g, '-');
    XLSX.writeFile(wb, marcaNome + '_' + dataFormatada + '.xlsx');
  }
"@

        $content = $content -replace '(?s)function exportarExcel\(\)\s*\{.*?(?=\n\s*function|\n\s*window|\n</script>)', "$newFunc`n`n"
        Set-Content -Path $file.FullName -Value $content
    }
}
