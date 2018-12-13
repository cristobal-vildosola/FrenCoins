# transforma el juego en un .exe

echo "Empezando freeze (no module named win32 found es normal)"
pyinstaller --add-data="static;static" -i "static\img\FrenCoin.ico" -F -w --distpath "." --log-level "ERROR" FrenCoins.py

# eliminar contenido generado
rm -rf build/
rm FrenCoins.spec

echo "Freeze completado con éxito, presiona una tecla para terminar"
read -n 1 -s
