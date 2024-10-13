
import os
import markdown
from datetime import datetime
from bs4 import BeautifulSoup

def convert_md_to_html(md_content):
    return markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])

def generate_blog_html(posts):
    blog_html = '''
    <section class="blog-posts">
        <h2 class="blog-title">My Blog Posts</h2>
    '''
    for post in posts:
        blog_html += f'''
        <article class="blog-post">
            <h3 class="post-title">{post['title']}</h3>
            <p class="post-meta">Posted on <time datetime="{post['date']}">{post['date']}</time></p>
            <div class="post-content">
                {post['content']}
            </div>
        </article>
        '''
    blog_html += '</section>'
    return blog_html

def update_blog_page(blog_content):
    with open('blog.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    main_div = soup.find('div', role='main')
    if main_div:
        main_div.clear()
        main_div.append(BeautifulSoup(blog_content, 'html.parser'))
    else:
        print("Could not find the main content div. Please check your HTML structure.")
        return

    with open('blog.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

def main():
    posts = []
    for filename in os.listdir('blog_posts'):
        if filename.endswith('.md'):
            with open(os.path.join('blog_posts', filename), 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.split('\n')
                title = lines[0].replace('# ', '')
                date_line = next((line for line in lines if line.startswith('Posted on ')), None)
                if date_line:
                    date = date_line.replace('Posted on ', '')
                    content = '\n'.join(lines[2:])  # Skip title and date lines
                else:
                    date = datetime.fromtimestamp(os.path.getmtime(os.path.join('blog_posts', filename))).strftime('%Y-%m-%d')
                    content = '\n'.join(lines[1:])  # Skip only title line
                
                html_content = convert_md_to_html(content)
                posts.append({'title': title, 'date': date, 'content': html_content})
    
    posts.sort(key=lambda x: x['date'], reverse=True)
    blog_html = generate_blog_html(posts)
    update_blog_page(blog_html)
    print("Blog updated successfully!")

if __name__ == "__main__":
    main()
