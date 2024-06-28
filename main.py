from flask import Flask, render_template, request, send_from_directory,redirect,url_for


app = Flask(__name__)


saved_memes = []

#----------------------------------------------------------------------------------
# Meme Form Sonuçları
#---------------------------------------------------------------------------------- 

@app.route('/meme', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # Seçilen Resmi Alır
        selected_image = request.form.get('image-selector')

        # Metni Alır
        text_top = request.form.get('textTop')
        text_bottom = request.form.get('textBottom')

        # Metnin Konumunu Alır
        selected_color = request.form.get('color-selector')

        # Metnin Rengini Alır
        text_top_y = request.form.get('textTop_y')
        text_bottom_y = request.form.get('textBottom_y')

        return render_template('index.html', 
                               # Seçilen Resmi Görüntüleme
                               selected_image=selected_image, 

                               # Metni Görüntüleme
                               text_top = text_top,
                               text_bottom = text_bottom,

                               # Rengi Görüntüleme
                               selected_color = selected_color,
                               
                               # Metnin Konumunu Görüntüleme
                               text_top_y = text_top_y,
                               text_bottom_y = text_bottom_y

                               )
    else:
        # Varsayılan Olarak İlk Resmi Görüntüleme
        return render_template('index.html', selected_image='logo.svg')



@app.route('/static/img/<path:path>')
def serve_images(path):
    return send_from_directory('static/img', path)


#----------------------------------------------------------------------------------
# Ana Sayfa
#----------------------------------------------------------------------------------

@app.route('/')
def anasayfa():
    return render_template('anasayfa.html')

#----------------------------------------------------------------------------------
# Koleksiyon
#----------------------------------------------------------------------------------

@app.route('/save_meme', methods=['POST'])
def save_meme():
    selected_image = request.form.get('selected_image')
    text_top = request.form.get('text_top')
    text_bottom = request.form.get('text_bottom')
    selected_color = request.form.get('selected_color')
    text_top_y = request.form.get('text_top_y')
    text_bottom_y = request.form.get('text_bottom_y')

    meme_data = {
        'selected_image': selected_image,
        'text_top': text_top,
        'text_bottom': text_bottom,
        'selected_color': selected_color,
        'text_top_y': text_top_y,
        'text_bottom_y': text_bottom_y
    }

    saved_memes.append(meme_data)

    return redirect(url_for('koleksiyon'))


@app.route('/koleksiyon')
def koleksiyon():
    return render_template('koleksiyon.html', saved_memes=saved_memes)


#----------------------------------------------------------------------------------
# Koleksiyon Silme İşlemi
#----------------------------------------------------------------------------------

@app.route('/delete_meme', methods=['POST'])
def delete_meme():
    if request.method == 'POST':
        selected_image = request.form.get('selected_image')

        # Seçilen resmi koleksiyondan kaldır
        for meme in saved_memes:
            if meme['selected_image'] == selected_image:
                saved_memes.remove(meme)
                break

    return redirect(url_for('koleksiyon'))


#----------------------------------------------------------------------------------
# Geri Bildirim Sayfası Ve Verileri Kaydetme
#----------------------------------------------------------------------------------

@app.route('/geribildirim', methods=['GET', 'POST'])
def geribildirim():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        with open("geribildirim.txt", "a") as f:
            f.write(f"Adı Soyadı = {name}\n")
            f.write(f"E-posta Adresi = {email}\n")
            f.write(f"Mesaj = {message}\n\n")

        return render_template('geribildirim.html', success=True)

    return render_template('geribildirim.html', success=False)

#------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)

