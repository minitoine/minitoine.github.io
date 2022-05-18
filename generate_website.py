import os
import yaml
from bs4 import BeautifulSoup

data = None

link_types_order = ['doi', 'pdf', 'video', 'presentation', 'github', 'code', 'demo',
    'linkedin','facebook','mail', 'resume']

def get_links_html(links, filter_links=link_types_order):

    template = get_template('link-template')

    html = ""

    linkMap = {}

    for link in links:
        if link['type'] in filter_links:
            linkMap[link['type']] = link;

    for link_type in link_types_order:
        if link_type in linkMap:

            link = linkMap[link_type]

            html += template.format(
                url = link.get('url', ''),
                fa_class = data['link_classes'][link_type],
                name = link.get('name', link_type)
            )
    return html

def get_authors_item_html(authors):
    htmls = []
    for p_author in authors:
        author = data.get("people").get(p_author)
        website = author.get("website", "")
        href = ""
        if not website == "":
            href = "href=\"{website}\"".format(website=website)
        htmls.append('<a {href}>{name}</a>'.format(href=href, name= author["name"]))
    html = ', '.join(htmls)
    return html

def get_keywords_html(keywords):

    template = get_template("keyword-template")
    html = "";

    for keyword in keywords:
        html += template.format(
            label = keyword
        )
    return html


def get_project_item_html(project):

    project_data = data[project]

    links = project_data["links"]
    code_links_type = ['github', 'code', 'demo', 'video']
    code_links = [link for link in links if link['type'] in code_links_type]
    publi_links = [link for link in links if link['type'] not in code_links_type]


    detailsclass = "nodisplay"
    if len(publi_links) > 0 or project_data.get("paper_title"):
        detailsclass = ""

    subtitle = project_data.get("year", "")
    location = project_data.get("location", "")
    if not location == "":
        subtitle += ', '+location


    links_html = get_links_html(publi_links)
    code_links_html = get_links_html(code_links)

    template = get_template('project-item-template')
    html = template.format(
        image = project_data["icon"],
        title = project_data["title"],
        location = project_data["location"],
        status = project_data["status"],
        detailsclass = detailsclass,
        publication = project_data.get("paper_title", ""),
        conf_short = project_data.get("conf_short", ""),
        subtitle = subtitle,
        summary = project_data["summary"],
        paper_links = links_html,
        project_links = code_links_html,
        keywords = get_keywords_html(project_data["keywords"])
    )
    return html


def get_position_item_html(position_data):
    template = get_template('position-item-template')
    html = template.format(
        position = position_data["position"],
        date = position_data["date"],
        location = position_data["location"],
        team = position_data["team"],

    )
    return html


def get_aboutme_item_html(aboutme_data):
    template = get_template('aboutme-template')
    html = template.format(
        image = aboutme_data["image"],
        catchphrase = aboutme_data["catchphrase"],
        name = aboutme_data["name"],
        text = aboutme_data["text"],
        links = get_links_html(aboutme_data["links"])
    )
    return html


def get_publication_item_html(publication):

    publication_data = data[publication]

    template = get_template('publication-item-template')
    html = template.format(
        image = publication_data["icon"],
        title = publication_data["paper_title"],
        conf_short = publication_data["conf_short"],
        authors = get_authors_item_html(publication_data.get("authors")),
        conference_info = publication_data["conf_long"],
        links = get_links_html(publication_data["links"]),
    )
    return html

def get_education_item_html(item_data):

    template = get_template('education-item-template')
    html = template.format(
        diploma = item_data["diploma"],
        location = item_data["location"],
        date = item_data["date"],
        text = item_data["text"],
    )
    return html

def get_template(id):
    template = soup.find(id=id)
    return str(template.div or template.a or template.span)

def get_items_html(items, item_func, sort_func=None):

    if sort_func:
        sort_func(items)

    html = ""
    for item in items:
        html += item_func(item)
    return html


def get_subsection_html(subsection_data, item_func, sort_func=None):

    items = subsection_data.get("items", [])
    content = get_items_html(items, item_func, sort_func)

    template = get_template("subsection-template")
    html = template.format(
        title = subsection_data.get("name"),
        content = content
    )
    return html

def get_section_html(section_data, item_func, sort_func=None):

    content = ''
    if section_data.get("subsections"):
        for subsection_data in section_data.get("subsections"):
            content += get_subsection_html(subsection_data, item_func, sort_func)
    else:
        items = section_data.get("items", [])
        content += get_items_html(items, item_func, sort_func)


    template = get_template("section-template")
    html = template.format(
        title = section_data.get("name"),
        content = content
    )
    return html


if __name__ == '__main__':
    f = open('data.yml', 'r')
    data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    f = open('template.html', 'r')
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()

    print("Generating AboutMe section...")
    section = soup.find(id='aboutme')
    html = get_aboutme_item_html(data['aboutme'])
    section.append(BeautifulSoup(html, 'html.parser'))

    def sortProjectsFunc(items):
        print(items)
        items.sort(key=lambda x: data.get(x).get('year'), reverse=True)

    print("Generating Projects section...")
    section = soup.find(id='projects')
    html = get_section_html(data['projects'], get_project_item_html, sortProjectsFunc)
    section.append(BeautifulSoup(html, 'html.parser'))

    print("Generating Education section...")
    section = soup.find(id='education')
    html = get_section_html(data['education'], get_education_item_html)
    section.append(BeautifulSoup(html, 'html.parser'))

    print("Generating Research section...")
    section = soup.find(id='research')
    html = get_section_html(data['research'], get_publication_item_html)
    section.append(BeautifulSoup(html, 'html.parser'))

    print("Generating Positions section...")
    section = soup.find(id='positions')
    html = get_section_html(data['positions'], get_position_item_html)
    section.append(BeautifulSoup(html, 'html.parser'))


    f = open('index.html', 'w')
    f.write(soup.prettify())
    f.close()

    print('Done.')

    
    