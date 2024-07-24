# Usa una imagen base de Windows Server Core
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . .

# Descarga e instala Python usando PowerShell
RUN powershell -Command \
    $ErrorActionPreference = 'Stop'; \
    $ProgressPreference = 'SilentlyContinue'; \
    Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.13/python-3.10.13-amd64.exe' -OutFile 'python-installer.exe'; \
    Start-Process -FilePath 'python-installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait; \
    Remove-Item -Force 'python-installer.exe'

# Instala las dependencias de Python
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar tu aplicación
CMD ["python", "apoyo_diagnostico.py"]

