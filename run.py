from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "═" * 70)
    print("   MODE DEVELOPMENT — AUTO-RELOAD AKTIF!")
    print("   Edit file .html → langsung update tanpa restart")
    print("   HTTPS + gembok hijau aktif")
    print("   Buka: https://localhost:5000")
    print("═" * 70 + "\n")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,                    
        use_reloader=True,             
        ssl_context=('localhost+1.pem', 'localhost+1-key.pem')
    )