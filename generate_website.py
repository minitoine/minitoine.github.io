import os
import yaml
from bs4 import BeautifulSoup

links_order = ['doi', 'pdf', 'video', 'presentation', 'github', 'code',
    'linkedin','facebook','mail', 'resume']

def get_fontawesome_icon_for_link_type(link_type):
    if link_type == 'doi':
        return 'fas fa-link'
    elif link_type == 'pdf':
        return 'fas fa-file-pdf'
    elif link_type == 'video':
        return 'fab fa-youtube'
    elif link_type == 'github':
        return 'fab fa-github'
    elif link_type == 'presentation':
        return 'fab fa-slideshare'
    elif link_type == 'code':
        return 'fas fa-download'
    elif link_type == 'mail':
        return 'fas fa-envelope-square'
    elif link_type == 'linkedin':
        return 'fab fa-linkedin'
    elif link_type == 'facebook':
        return 'fab fa-facebook-square'
    elif link_type == 'resume':
        return 'fas fa-portrait'

def get_links_html(links):
    html = '<ul class="social">'
    for link in links_order:
        if link in links:
            url = links[link]
            html += '''
            <li>
                <a href="{url}">
                    <i class="{fontawesome_icon}"></i>
                    <span class="label">{name}</span>
                </a>
            </li>'''.format(
                url = url,
                fontawesome_icon = get_fontawesome_icon_for_link_type(link),
                name = link)
    html += "</ul>"
    return html

def get_authors_list_html(data, authors):
    html = ''
    cpt = 0
    for p_author in authors:
        author = data.get("people").get(p_author)
        if 'website' in author:
            html += '<a href="{website}">{name}</a>'.format(
                website=author.get("website"), name= author.get("name"))
        else:
            html += author.get('name')
        cpt += 1
        if cpt < len(authors):
            html += ', '
    return html

def get_project_item_html(data, project):
    return '''
    <div class="row myrow" id="article_item">
        <img class="1u mycol" alt="" src="images/{icon}"/>
        <div class="11u mycol colAfterImage">
            <div>
                <b>{title}</b>
            </div>
            <div>
                <i>{year}, {duration}. {status}, {location}</i>
            </div>
            <div style="text-align: justify; text-justify: inter-word;">
                {text} <i>[{technologies}]<i>
            </div>
            <div>
                {links}
            </div>
        </div>
    </div>'''.format(
        icon = project["icon"],
        title = project["title"],
        year = project["year"],
        duration = project["duration"],
        status = project["status"],
        location = project["location"],
        text = project["text"],
        technologies = project["technologies"],
        links = get_links_html(project["links"]))

def get_publication_item_html(data, publication):
    return '''
    <div class="row myrow" id="article_item">
        <img class="1u mycol" alt="" src="images/{icon}"/>
        <div class="11u mycol colAfterImage">
            <div>
                <b>{title}</b>
            </div>
            <div>
                <i>{conf_short}{presenter}</i>
            </div>
            <div>
                <i>{authors}</i>
            </div>
            <div style="text-align: justify; text-justify: inter-word;">
                {conference}
            </div>  
            <div>
                {links}
            </div>
        </div>
    </div>'''.format(
        icon = publication["icon"],
        title = publication["title"],
        conf_short = publication["conf_short"],
        presenter = ', Presenter' if publication.get('presenter') else '',
        authors = get_authors_list_html(data, publication.get("authors")),
        conference = publication["conf_long"],
        links = get_links_html(publication["links"]))

def get_infos_html(infos):
    return '''
    <div class="container">
        <div class="row myrow">
            <image class="3u mycol" alt="" src="images/{image}" style="border-radius: 50%;"/>
            <div class="9u mycol">
                <h3> {name} </h3>
                <p style="text-align: justify; text-justify: inter-word;">
                    {text}
                </p>
               {links} 
            </div>
        </div>
    </div>
    '''.format(
        image = infos["image"],
        name = infos["name"],
        text = infos["text"],
        links = get_links_html(infos["links"])
    )

def get_text_item_html(data, item):
    html = '''
    <div class="row myrow" id="article_item">
        <div class="2u mycol" id="article_year">
            {years}
            <br>
            <i>{extra_infos}</i>
        </div>  
        <div class="10u mycol">
            <div><b>{title}</b></div>
            <div>{text}</div>
        </div>
    </div>'''.format(
        title = item.get("title", ""),
        years = item.get("years", ""),
        extra_infos = item.get("extra_infos", ""),
        text = item.get("text", "")
    )
    return html

def get_section_html(data, section_id, item_func):

    section_data = data[section_id]

    content = ''
    if "subsections" in section_data:
        for subsection, sub_data in section_data.get("subsections").items():
            content += '<h4>%s</h4>'%sub_data.get("name")
            items = sub_data.get("items", [])
            for item in items:
                content += item_func(data, item)
    else:
        items = section_data.get("items")
        for item in items:
            content += item_func(data, item)        

    html = '''
    <article>
        <div class="container">
            <h3>{title}</h3>
            {content}
        </div>
    </article>
    '''.format(
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

    projects = soup.find(id='home')
    projects.append(BeautifulSoup(get_infos_html(data["infos"]), 'html.parser'))

    print("Generating Projects section...")
    projects = soup.find(id='projects')
    projects.append(BeautifulSoup(get_section_html(
        data, 'projects', get_project_item_html), 'html.parser'))

    print("Generating Publications section...")
    projects = soup.find(id='publications')
    projects.append(BeautifulSoup(get_section_html(
        data, 'publications', get_publication_item_html), 'html.parser'))

    print("Generating Education section...")
    projects = soup.find(id='education')
    projects.append(BeautifulSoup(get_section_html(
        data, 'education', get_text_item_html), 'html.parser'))

    print('Generating Experience section...')
    projects = soup.find(id='experience')
    projects.append(BeautifulSoup(get_section_html(
        data, "experience", get_text_item_html), "html.parser"))


    
    f = open('index.html', 'w')
    f.write(soup.prettify())
    f.close()

    print('Done.')

    
    