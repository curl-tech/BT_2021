git submodule update --recursive

cd cycle_gan
pip install -r requirements.txt

bash ./scripts/download_cyclegan_model.sh style_vangogh
bash ./scripts/download_cyclegan_model.sh style_cezanne

cd ..

