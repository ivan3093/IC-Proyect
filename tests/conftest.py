# tests/conftest.py
import os
import pytest

@pytest.fixture
def tmp_template_dir(tmp_path):
    """Crea un directorio temporal con un template Jinja2 que cubre
    conteos, top (lista o dict) y secciones de muestras."""
    tpl_dir = tmp_path / "templates"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    (tpl_dir / "report.html.j2").write_text(
        """<!doctype html>
        <html><body>
        <h1>Report</h1>

        <!-- Totales (usado por los tests) -->
        <p>ERROR: {{ metrics.counts.ERROR }}</p>
        <p>WARNING: {{ metrics.counts.WARNING }}</p>
        <p>INFO: {{ metrics.counts.INFO }}</p>

        <img src="{{ chart_filename }}" />

        <h2>Top repetidos</h2>
        <table>
          <tr><th>Nivel</th><th>Mensaje</th><th>Conteo</th></tr>

          {# --- TOP ERROR --- #}
          {% set err_top = metrics.top.ERROR %}
          {% if err_top is mapping %}
            <tr>
              <td>ERROR</td>
              <td>{{ err_top.message }}</td>
              <td>{{ err_top.count }}</td>
            </tr>
          {% elif err_top is sequence %}
            {% for item in err_top %}
              <tr>
                <td>ERROR</td>
                <td>{{ item.message }}</td>
                <td>{{ item.count }}</td>
              </tr>
            {% endfor %}
          {% else %}
            <tr><td>ERROR</td><td colspan="2">N/A</td></tr>
          {% endif %}

          {# --- TOP WARNING --- #}
          {% set warn_top = metrics.top.WARNING %}
          {% if warn_top is mapping %}
            <tr>
              <td>WARNING</td>
              <td>{{ warn_top.message }}</td>
              <td>{{ warn_top.count }}</td>
            </tr>
          {% elif warn_top is sequence %}
            {% for item in warn_top %}
              <tr>
                <td>WARNING</td>
                <td>{{ item.message }}</td>
                <td>{{ item.count }}</td>
              </tr>
            {% endfor %}
          {% else %}
            <tr><td>WARNING</td><td colspan="2">N/A</td></tr>
          {% endif %}
        </table>

        <h2>Muestras por severidad</h2>
        {% for level in ["ERROR", "WARNING", "INFO"] %}
          <h3>{{ level }}</h3>
          <h4>Primeras {{ samples[level]["first"] | length }}</h4>
          <table>
            <tr><th>#</th><th>Línea</th></tr>
            {% for line in samples[level]["first"] %}
            <tr><td>{{ loop.index }}</td><td><code>{{ line }}</code></td></tr>
            {% endfor %}
          </table>

          <h4>Últimas {{ samples[level]["last"] | length }}</h4>
          <table>
            <tr><th>#</th><th>Línea</th></tr>
            {% for line in samples[level]["last"] %}
            <tr><td>{{ loop.index }}</td><td><code>{{ line }}</code></td></tr>
            {% endfor %}
          </table>
        {% endfor %}

        </body></html>
        """,
        encoding="utf-8",
    )
    return tpl_dir

@pytest.fixture(autouse=True)
def cwd_tmp(tmp_path):
    """
    Aísla el CWD en un tmp por prueba, para que 'static/reports' no ensucie el repo.
    Si ya tuvieras otra fixture 'cwd_tmp' en root, NO dupliques esta.
    """
    old = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield
    finally:
        os.chdir(old)
