import glob, re

NEW_FN = r'''function exportarExcel() {
    if (codigos.length === 0) {
      alert('Nenhum código para exportar.');
      return;
    }

    const marcaNome = "__MARCA__";
    let esperado = 0;
    try {
      const esperadoPorMarca = JSON.parse(localStorage.getItem('esperado_por_marca') || '{}');
      esperado = esperadoPorMarca[marcaNome] || 0;
    } catch (e) {}

    const lido = codigos.length;
    const faltam = esperado - lido;
    const dataHoje = new Date().toLocaleDateString('pt-BR');

    // ---------- estilos ----------
    const lado = { style: 'thin', color: { rgb: 'BFBFBF' } };
    const borda = { top: lado, bottom: lado, left: lado, right: lado };
    const centro = { horizontal: 'center', vertical: 'center' };
    const sCab = { font: { bold: true, color: { rgb: 'FFFFFF' }, sz: 12 }, fill: { fgColor: { rgb: '007BFF' } }, alignment: centro, border: borda };
    const sTitulo = { font: { bold: true, sz: 16, color: { rgb: '004692' } }, alignment: { horizontal: 'left', vertical: 'center' } };
    const sSub = { font: { italic: true, color: { rgb: '666666' } }, alignment: { horizontal: 'left' } };
    const cab = t => ({ v: t, t: 's', s: sCab });
    const txt = (v, fill) => ({ v: String(v), t: 's', s: { alignment: centro, border: borda, fill: fill ? { fgColor: { rgb: fill } } : undefined } });
    const num = (v, fill, bold, cor) => ({ v: v, t: 'n', s: { alignment: centro, border: borda, font: { bold: !!bold, sz: bold ? 13 : 11, color: cor ? { rgb: cor } : undefined }, fill: fill ? { fgColor: { rgb: fill } } : undefined } });

    const corFaltam = faltam <= 0 ? 'C6EFCE' : 'FFC7CE';
    const corTxtFaltam = faltam <= 0 ? '006100' : '9C0006';

    // ---------- uma única aba: resumo em cima, lista embaixo ----------
    const aoa = [
      [{ v: marcaNome, t: 's', s: sTitulo }],
      [{ v: 'Gerado em ' + dataHoje, t: 's', s: sSub }],
      [],
      [cab('Esperado'), cab('Lido'), cab('Faltam')],
      [num(esperado, null, true), num(lido, null, true), num(faltam, corFaltam, true, corTxtFaltam)],
      [],
      [cab('#'), cab('Código'), cab('Hora')]
    ];
    const linhaCab = aoa.length; // número (1-based) da linha do cabeçalho da lista
    codigos.forEach((c, i) => {
      const zebra = i % 2 === 1 ? 'F2F7FF' : null;
      aoa.push([ num(i + 1, zebra), txt(c.codigo, zebra), txt(c.hora, zebra) ]);
    });

    const ws = XLSX.utils.aoa_to_sheet(aoa);
    const maxCod = Math.max(18, ...codigos.map(c => String(c.codigo).length)) + 4;
    ws['!cols'] = [{ wch: 14 }, { wch: maxCod }, { wch: 18 }];
    ws['!merges'] = [{ s: { r: 0, c: 0 }, e: { r: 0, c: 2 } }, { s: { r: 1, c: 0 }, e: { r: 1, c: 2 } }];
    ws['!autofilter'] = { ref: 'A' + linhaCab + ':C' + aoa.length };
    ws['!rows'] = [{ hpt: 26 }, {}, {}, { hpt: 22 }, { hpt: 24 }, {}, { hpt: 22 }];

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Contagem');

    const dataArq = dataHoje.replace(/\//g, '-');
    XLSX.writeFile(wb, marcaNome.replace(/\s+/g, '_') + '_' + dataArq + '.xlsx');
  }

  
'''

SCRIPT_OLD = '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>'
SCRIPT_NEW = '<script src="https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.bundle.js"></script>'

# Magnum estava corrompido: recria a partir de um modelo saudável
base = open('adidas.html', encoding='utf-8').read()
mag = base.replace('Adidas', 'Magnum').replace('codigos_adidasc', 'codigos_magnumm')
open('magnum.html', 'w', encoding='utf-8').write(mag)

for f in glob.glob('*.html'):
    if f == 'index.html':
        continue
    s = open(f, encoding='utf-8').read()
    m = re.search(r'const marcaNome = "([^"]+)"', s)
    if not m:
        print('PULOU', f); continue
    fn = NEW_FN.replace('__MARCA__', m.group(1))
    s = re.sub(r'function exportarExcel\(\) \{.*?(?=window\.addEventListener\(\'click\')', lambda _: fn, s, flags=re.S)
    s = s.replace(SCRIPT_OLD, SCRIPT_NEW)
    open(f, 'w', encoding='utf-8').write(s)
    print('OK', f)


IDX_FN = r"""function exportarExcel() {
    const esperadoTotal = parseInt(localStorage.getItem("esperado_total")) || 0;
    const esperadoPorMarca = JSON.parse(localStorage.getItem("esperado_por_marca") || "{}");
    const lado = { style: 'thin', color: { rgb: 'BFBFBF' } };
    const borda = { top: lado, bottom: lado, left: lado, right: lado };
    const centro = { horizontal: 'center', vertical: 'center' };
    const sCab = { font: { bold: true, color: { rgb: 'FFFFFF' }, sz: 12 }, fill: { fgColor: { rgb: '007BFF' } }, alignment: centro, border: borda };
    const cab = t => ({ v: t, t: 's', s: sCab });
    const txt = (v, fill, bold) => ({ v: String(v), t: 's', s: { alignment: centro, border: borda, font: { bold: !!bold }, fill: fill ? { fgColor: { rgb: fill } } : undefined } });
    const num = (v, fill, bold, cor) => ({ v: v, t: 'n', s: { alignment: centro, border: borda, font: { bold: !!bold, color: cor ? { rgb: cor } : undefined }, fill: fill ? { fgColor: { rgb: fill } } : undefined } });

    const det = [[cab('Marca'), cab('#'), cab('Código'), cab('Hora')]];
    const res = [[cab('Marca'), cab('Esperado'), cab('Lido'), cab('Faltam')]];
    let totalLido = 0, maxCod = 18, z = 0;

    marcas.forEach(m => {
      const codigos = getLista(m.chave);
      const esperado = esperadoPorMarca[m.nome] || 0;
      const faltam = esperado - codigos.length;
      totalLido += codigos.length;
      if (esperado > 0 || codigos.length > 0) {
        res.push([txt(m.nome), num(esperado), num(codigos.length),
                  num(faltam, faltam <= 0 ? 'C6EFCE' : 'FFC7CE', true, faltam <= 0 ? '006100' : '9C0006')]);
      }
      codigos.forEach((c, i) => {
        const f = (z++ % 2) ? 'F2F7FF' : null;
        maxCod = Math.max(maxCod, String(c.codigo).length + 4);
        det.push([txt(m.nome, f), num(i + 1, f), txt(c.codigo, f), txt(c.hora, f)]);
      });
    });

    if (det.length === 1 && res.length === 1) { alert("Nenhum dado para exportar."); return; }

    const f = esperadoTotal - totalLido;
    res.push([txt('TOTAL GERAL', 'DDEBF7', true), num(esperadoTotal, 'DDEBF7', true), num(totalLido, 'DDEBF7', true),
              num(f, f <= 0 ? 'C6EFCE' : 'FFC7CE', true, f <= 0 ? '006100' : '9C0006')]);

    const wb = XLSX.utils.book_new();
    const wsDet = XLSX.utils.aoa_to_sheet(det);
    wsDet['!cols'] = [{ wch: 20 }, { wch: 8 }, { wch: maxCod }, { wch: 16 }];
    wsDet['!autofilter'] = { ref: 'A1:D' + det.length };
    wsDet['!rows'] = [{ hpt: 24 }];
    XLSX.utils.book_append_sheet(wb, wsDet, 'Detalhes');
    const wsRes = XLSX.utils.aoa_to_sheet(res);
    wsRes['!cols'] = [{ wch: 25 }, { wch: 15 }, { wch: 15 }, { wch: 15 }];
    XLSX.utils.book_append_sheet(wb, wsRes, 'Resumo');

    const dataFormatada = new Date().toLocaleDateString("pt-BR").replace(/\//g, '-');
    XLSX.writeFile(wb, `Relatorio_Geral_${dataFormatada}.xlsx`);
  }

  """
s=open('index.html',encoding='utf-8').read()
s=re.sub(r'function exportarExcel\(\) \{.*?(?=function limpar\(\) \{)', lambda _: IDX_FN, s, flags=re.S)
s=s.replace(SCRIPT_OLD, SCRIPT_NEW)
open('index.html','w',encoding='utf-8').write(s)
print('OK index')
