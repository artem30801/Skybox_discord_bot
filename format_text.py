import win32clipboard
import HTMLClipboard

if __name__ == '__main__':
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    html = HTMLClipboard
    print(data)
    chtml = '<text style="font-family:v_Comic Geek; font-size:4pt; font-size-adjust:0.717919; text-anchor:middle"><tspan x="0">{}'\
            '</tspan></text>'.format(data)
    HTMLClipboard.PutHtml(chtml)
