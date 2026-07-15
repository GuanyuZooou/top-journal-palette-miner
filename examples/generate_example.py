from pathlib import Path

from PIL import Image, ImageDraw


output = Path(__file__).with_name("synthetic-scientific-figure.png")
image = Image.new("RGB", (960, 540), "#FAFAF8")
draw = ImageDraw.Draw(image)
draw.line((100, 450, 880, 450), fill="#606060", width=4)
draw.line((100, 70, 100, 450), fill="#606060", width=4)
blue = [(120 + i * 70, 380 - i * 28) for i in range(10)]
rose = [(120 + i * 70, 410 - i * 18) for i in range(10)]
draw.line(blue, fill="#4D779B", width=8)
draw.line(rose, fill="#C45C69", width=8)
for point in blue:
    draw.ellipse((point[0] - 7, point[1] - 7, point[0] + 7, point[1] + 7), fill="#4D779B")
for point in rose:
    draw.rectangle((point[0] - 6, point[1] - 6, point[0] + 6, point[1] + 6), fill="#C45C69")
draw.ellipse((740, 105, 770, 135), fill="#FFC04D", outline="#606060", width=2)
draw.line((755, 135, 755, 450), fill="#FFC04D", width=5)
image.save(output)
print(output.name)
