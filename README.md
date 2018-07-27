# toBraille
***
使用此模组之前，请使用pip install xpinyin安装xpinyin模组。xpinyin模组使用方法，请自行百度，谢谢。
这是一组将汉字转化成盲文ascii码，以及盲文点数的程序。
你可以这样用:
from toBrialle import toBraille

braille_dots = toBraille('小风')
print(braille_dots)

然后它就会显示：
('h>f#', '125-345-124-3456')
这样的结果。
前面的元素是他的代码， 后面的一串是将要在点显器上显示或者只在纸上扎的点位。
剩下的留给你自己去尝试了

注意：要用toBraille一定要下载我的dotsBraille， 因为我在toBraille里面引用了它。你也可以不下载，尝试改改代码也是行的通的。
