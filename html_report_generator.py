from datetime import datetime

class HTMLReportGenerator:
    @staticmethod
    def generate(stats):
        total_urls = len(stats)
        total_valid = sum(s['valid'] for s in stats.values())
        total_removed = sum(s['removed'] for s in stats.values())
        total_absolute = sum(s['absolute'] for s in stats.values())
        total_relative = sum(s['relative'] for s in stats.values())

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Отчёт краулера</title>
            <style>
                * {{ box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f4f7fb; color: #1e2a3a; }}
                .container {{ max-width: 1400px; margin: 0 auto; }}
                h1 {{ color: #1e2a3a; border-bottom: 3px solid #3b82f6; padding-bottom: 10px; margin-top: 0; }}
                .summary {{ display: flex; gap: 15px; flex-wrap: wrap; margin: 20px 0; }}
                .card {{ background: white; padding: 12px 24px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); flex: 1 1 140px; }}
                .card h3 {{ margin: 0; font-weight: 400; font-size: 0.9em; color: #64748b; }}
                .card .number {{ font-size: 2em; font-weight: 700; color: #0f172a; }}
                table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
                th {{ background: #f1f5f9; color: #1e293b; font-weight: 600; padding: 12px 16px; text-align: left; }}
                td {{ padding: 10px 16px; border-bottom: 1px solid #e9edf2; vertical-align: middle; }}
                .main-row {{ cursor: default; }}
                .main-row td {{ border-bottom: none; }}
                .detail-row {{ display: none; }}
                .detail-row.open {{ display: table-row; }}
                .detail-row td {{ padding: 0; background: #f8fafc; border-bottom: 1px solid #e9edf2; }}
                .detail-content {{ padding: 16px 20px; }}
                .badge {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.85em; font-weight: 500; }}
                .badge-success {{ background: #d1fae5; color: #065f46; }}
                .badge-danger {{ background: #fee2e2; color: #991b1b; }}
                .badge-warning {{ background: #fef3c7; color: #92400e; }}
                .badge-info {{ background: #dbeafe; color: #1e40af; }}
                .toggle-links {{ cursor: pointer; color: #3b82f6; font-weight: 500; user-select: none; }}
                .toggle-links:hover {{ text-decoration: underline; }}
                .links-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .links-column {{ background: white; border-radius: 8px; padding: 10px; border: 1px solid #e2e8f0; overflow-y: auto; max-height: 350px; }}
                .links-column h4 {{ margin: 0 0 8px 0; font-size: 0.95em; }}
                .links-column ul {{ margin: 0; padding: 0; list-style: none; }}
                .links-column li {{ padding: 4px 6px; font-family: monospace; font-size: 0.85em; border-bottom: 1px solid #f1f5f9; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
                .links-column li:last-child {{ border-bottom: none; }}
                .url-cell {{ max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
                .footer {{ margin-top: 30px; text-align: center; color: #94a3b8; font-size: 0.9em; }}
                @media (max-width: 700px) {{
                    .links-grid {{ grid-template-columns: 1fr; }}
                    .summary .card {{ flex: 1 1 100%; }}
                }}
            </style>
            <script>
                function toggleDetail(id) {{
                    var row = document.getElementById(id);
                    if (row) {{
                        row.classList.toggle('open');
                    }}
                }}
            </script>
        </head>
        <body>
        <div class="container">
            <h1>📊 Отчёт краулера</h1>
            <div class="summary">
                <div class="card"><h3>Всего URL</h3><div class="number">{total_urls}</div></div>
                <div class="card"><h3>Валидных ссылок</h3><div class="number">{total_valid}</div></div>
                <div class="card"><h3>Удалённых ссылок</h3><div class="number">{total_removed}</div></div>
                <div class="card"><h3>Абсолютных</h3><div class="number">{total_absolute}</div></div>
                <div class="card"><h3>Относительных</h3><div class="number">{total_relative}</div></div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>Валидные</th>
                        <th>Абсолютные</th>
                        <th>Относительные</th>
                        <th>Удалённые</th>
                        <th style="width: 140px;">Детали</th>
                    </tr>
                </thead>
                <tbody>
        """

        for idx, (url, s) in enumerate(stats.items()):
            detail_id = f"detail_{idx}"
            valid_links = s.get('valid_links', [])
            removed_links = s.get('removed_links', [])
            html += f"""
                <tr class="main-row">
                    <td class="url-cell" title="{url}">{url}</td>
                    <td><span class="badge badge-success">{s['valid']}</span></td>
                    <td><span class="badge badge-info">{s['absolute']}</span></td>
                    <td><span class="badge badge-warning">{s['relative']}</span></td>
                    <td><span class="badge badge-danger">{s['removed']}</span></td>
                    <td>
                        <span class="toggle-links" onclick="toggleDetail('{detail_id}')">Показать ссылки</span>
                    </td>
                </tr>
                <tr id="{detail_id}" class="detail-row">
                    <td colspan="6">
                        <div class="detail-content">
                            <div class="links-grid">
                                <div class="links-column col-valid">
                                    <h4 style="color: #065f46;">✅ Валидные ({len(valid_links)})</h4>
                                    <ul>
            """
            if valid_links:
                for link in valid_links:
                    html += f"<li>{link}</li>"
            else:
                html += "<li style='color: #94a3b8; font-style: italic;'>Нет</li>"
            html += """
                                    </ul>
                                </div>
                                <div class="links-column col-removed">
                                    <h4 style="color: #991b1b;">❌ Удалённые ({count})</h4>
                                    <ul>
            """.replace("{count}", str(len(removed_links)))
            if removed_links:
                for link in removed_links:
                    html += f"<li>{link}</li>"
            else:
                html += "<li style='color: #94a3b8; font-style: italic;'>Нет</li>"
            html += """
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            """

        html += f"""
                </tbody>
            </table>
            <div class="footer">
                Отчёт сгенерирован {datetime.now().strftime("%d.%m.%Y %H:%M")}
            </div>
        </div>
        </body>
        </html>
        """
        return html