import os, markdown, shutil
from datetime import datetime

POSTS_DIR, STATIC_DIR, OUTPUT_DIR = "posts", "static", "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load(name):
    with open(os.path.join(STATIC_DIR, f"{name}.html"), "r", encoding="utf-8") as f:
        return f.read()

def tagextract(content):
    tags = {}
    for line in content.splitlines():
        if line.startswith("---"): continue
        if ":" in line:
            k, v = line.split(":", 1)
            tags[k.strip()] = v.strip()
    return tags

def tagremove(content):
    return "\n".join(l for l in content.splitlines() if not (l.startswith("---") or ":" in l))

def generate():
    header, footer = load("header"), load("footer")
    post_template, index_template = load("post"), load("index")
    posts = []
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".md"):
            with open(os.path.join(POSTS_DIR, file), "r", encoding="utf-8") as f:
                content = f.read()
                tags = tagextract(content)
                title, date = tags.get("title", file[:-3]), tags.get("date", datetime.now().strftime("%Y-%m-%d"))
                html = markdown.markdown(tagremove(content), extensions=["extra", "tables"])
                post = post_template.replace("{header}", header).replace("{footer}", footer).replace("{title}", title).replace("{date}", date).replace("{content}", html)
                with open(os.path.join(OUTPUT_DIR, file.replace(".md", ".html")), "w", encoding="utf-8") as f:
                    f.write(post)
                posts.append((title, date, file.replace(".md", ".html")))
    index = index_template.replace("{header}", header).replace("{footer}", footer).replace("{posts}", "<table class='posts'>" + "".join(f'<tr><td><a href="{l}">{t}</a></td><td>{d}</td></tr>' for t, d, l in posts) + "</table>")
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)
    for item in os.listdir(STATIC_DIR):
        if item not in {"header.html", "footer.html", "post.html", "index.html"}:
            s, d = os.path.join(STATIC_DIR, item), os.path.join(OUTPUT_DIR, item)
            shutil.copytree(s, d, dirs_exist_ok=True) if os.path.isdir(s) else shutil.copy2(s, d)

if __name__ == "__main__":
    generate()
    print("generated!")