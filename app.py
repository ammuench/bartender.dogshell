import os
import logging
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(filename='logfile.log', level=logging.INFO)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        cocktail = request.form["cocktail"]
        app.logger.info(cocktail)
        response_normal = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt_cocktails(cocktail),
            temperature=0.75,
            top_p=0.75,
            max_tokens=150
        )
        app.logger.info("Normal recipe:")
        app.logger.info(response_normal)

        response_absurd = openai.Completion.create(
            model="text-babbage-001",
            prompt=generate_prompt_cocktails(cocktail),
            temperature=1.5,
            top_p=0.9,
            max_tokens=150,
            # stop="Cocktail:"
        )
        app.logger.info("Absurd recipe:")
        app.logger.info(response_absurd)
        return redirect(url_for("index", result_normal=response_normal.choices[0].text, cocktail=cocktail, result_absurd=response_absurd.choices[0].text))

    return render_template("index.html", result_normal=request.args.get("result_normal"), result_absurd=request.args.get("result_absurd"), cocktail=request.args.get("cocktail"))


def generate_prompt_cocktails(cocktail_name: str):
    return """Suggest recipe for a cocktail.

Cocktail: Margarita
Recipe: 1 part Cazadores Tequila, ½ part triple sec liqueur, ½ part lime juice, 1 lime wedge, Salt, Cubed ice. Chill your glass (the easiest way is to fill it with ice). Put lots of ice and all of the ingredients into a shaker, then shake hard for about 30 seconds to chill the liquid really well. Run a lime wedge around the outside of the rim of your glass before rolling the rim in salt. Double strain the mix into the glass.
Cocktail: Cosmopolitan
Recipe: 45ml lemon vodka, 15ml triple sec, 30ml cranberry juice, 10ml lime juice, ice. For the garnish orange zest, or a lime wedge on the rim of the glass. Shake ingredients in a cocktail shaker with ice and strain into a cocktail glass. To make the garnish: hold a 3cm round piece of orange zest about 10cm above your cosmo and very carefully wave it over a lit match or lighter flame. Bend the outer edge of the zest in towards the flame so that the orange oils are released, then drop the zest into your drink.
Cocktail: Daiquiri
Recipe: 50ml white rum, 25ml lime juice, 10ml sugar syrup, ice. Shake all the ingredients in a cocktail shaker and strain into a cocktail glass.
Cocktail: Gimlet
Recipe: 2 1/2 ounces gin, 1/2 ounce lime juice, freshly squeezed, 1/2 ounce simple syrup, lime wheel. Add the gin, lime juice and simple syrup to a shaker with ice and shake until well-chilled. Strain into a chilled cocktail glass or an rocks glass filled with fresh ice. Garnish with a lime wheel.
Cocktail: {}
Recipe:""".format(cocktail_name.capitalize())
