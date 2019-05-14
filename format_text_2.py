import klembord

if __name__ == '__main__':
    klembord.init()
    text = klembord.get_text()
    print(text)
    html = '<text style="font-family:v_Comic Geek; font-size:4pt; font-size-adjust:0.717919; text-anchor:middle"><tspan x="0">{}' \
            '</tspan></text>'.format(text)
    klembord.set_with_rich_text(text, html)

