import { Component } from 'react';
import { ImageAside, Reel, Body, NavItem } from '../components';
import { Route, NavLink } from 'react-router-dom';
import { Slider } from '../../components/Carousel';

class FunderList extends Component {
  parseFunderList = (html, cols=2) => {
    let funders = this.getJSXFromHTML(html);
    let len = Math.ceil(funders.length/cols)-1;
    let groups = [];
    for(let i=0; i<cols; i++){
      let start = len*i + i*1;
      let end = i===cols-1 ? funders.length : len * (i+1) + 1;
      groups.push(funders.slice(start, end));
    }

    return groups;
    // this is what's happening:
    // return [
    //   funders.slice(0, len),
    //   funders.slice(len+1, len*2+1),
    //   funders.slice(len*2+2, funders.length-1),
    //
    //];
  }

  getJSXFromHTML = (html) => {
    let { type } = this.props;

    let div = document.createElement('div');
    div.innerHTML = html;
    let funders = div.getElementsByTagName('li');
    if(type === 'funder' )
      return Array.from(funders).map((f,i)=>(
        <label key={`funder-${i}`} className="block margin-top-0">{f.innerText}</label>
      ));

    return Array.from(funders).map((f,i)=>{
      let b = f.getElementsByTagName('b')[0];
      let name = b.innerText;
      let position = f.innerText.replace(name, '');

      return (
        <div className="our-funding__council-list__item margin-bottom-25" key={`funder-${i}`}>
          <label className="block bold margin-top-0 margin-bottom-5">{name}</label>
          {position.length > 0 && <label className="caption margin-top-5">{position}</label>}
        </div>
      );
    });
  }

  render(){
    let { paragraph, heading, intro, columns } = this.props;
    let groupedLists = this.parseFunderList(paragraph, columns);
    return (
      <div className="home__panel__funders-list margin-bottom-60" >
        <div className="row gutter-20">
          <div className="col-lg-7">
            {heading != 'NULL' && <h2 className="margin-bottom-25">{heading}</h2>}
            <div className="home__panel__funders-list__body" dangerouslySetInnerHTML={{__html: intro}} />
          </div>
        </div>
        <div className="row gutter-20">
          {groupedLists.map((g,i)=>(
            <div className="col-md-4" key={`list-${i}`}>
              <ul className="no-list-style">
                {g}
              </ul>
            </div>
          ))}
        </div>
      </div>
    );
  }
}

class OurFunderLists extends Component {

  render(){
    let { data : { donors_and_partners }, heading } = this.props;
    return (
      <section className="funders-list post-body container--1080 margin-80">
        <div className="row gutter-10">
          <div className="col-lg-7">
            <h1 className="margin-top-0">{heading}</h1>
          </div>
        </div>
        {donors_and_partners.heading.map((h,i)=>(
          <FunderList type="funder" key={`funder-${i}`}
            heading={h}
            paragraph={donors_and_partners.paragraph[i]}
            intro={donors_and_partners.introduction[i].indexOf("NULL")>=0 ? null : donors_and_partners.introduction[i]} />
        ))}
      </section>
    );
  }
}

class FunderLists extends Component {

  render(){
    let { data : { intro, circles } } = this.props;
    return (
      <section className="funders-list post-body container--1080 margin-80">
        <div className="row gutter-10">
          <div className="col-lg-7">
            {/* <h1 className="margin-top-0">{funders_intro.heading[0]}</h1> */}
            <div className="margin-bottom-35 home__panel__funders-list__body" dangerouslySetInnerHTML={{__html: intro.paragraph[0] }}/>
          </div>
        </div>
        {circles.heading.map((h,i)=>(
          <FunderList type="funder" key={`funder-${i}`}
            heading={h}
            paragraph={circles.paragraph[i]}
            intro={circles.introduction[i].indexOf("NULL")>=0 ? null : circles.introduction[i]} />
        ))}
      </section>
    );
  }
}

class Nav extends Component {

  render(){
    return (
      <div className={`container--1080 our-funding__nav program__nav margin-top-15`}>
        <ul className="inline">
          <Slider
              variableWidth={true}
              infinite={false}
              slide={'li'}
              prevArrow={<div></div>}
              nextArrow={<div></div>}
              responsive={[
                { breakpoint: 625, settings: { slidesToShow: 2, slidesToScroll: 1 } },
                { breakpoint: 1000000, settings: 'unslick' }
              ]}>
                <li><NavItem url={`/our-funding/`} exact={true} label="How We're Funded"/></li>
                <li><NavItem url={`/our-funding/our-funders/`} exact={true} label="Our Funders"/></li>
                <li><NavItem url={`/our-funding/corporate-circle/`} label="Corporate Circle"/></li>
                <li><NavItem url={`/our-funding/new-america-councils/`} label="New America Councils"/></li>
                <li><NavItem url={`/our-funding/donate/`} label="Donate"/></li>
              </Slider>
        </ul>
      </div>
    );
  }
}

class Councils extends Component {
  sectionIntro = (intro) => {
    return (
      <div className="our-funding__intro row gutter-20">
        <div className="col-lg-9">
          {intro.heading && <h1 className="margin-top-0 margin-bottom-25">{intro.heading[0]}</h1>}
          <p className="margin-top-25 margin-bottom-35" dangerouslySetInnerHTML={{__html: intro.introduction[0] }}/>
        </div>
      </div>
    );
  }
  render(){
    let { data : {
      intro,
      leadership_council_intro,
      leadership_council,
      network_councils_intro,
      network_councils,
      program_councils_intro,
      program_councils,
      circles
    }} = this.props;
    return (
      <section className="container--1080 our-funding__circles_and_councils margin-80">
        {this.sectionIntro(leadership_council_intro)}
        <div className="our-funding__council">
          {leadership_council.heading.map((h,i)=>(
            <FunderList type="council" columns={2} key={`funder-${i}`}
              heading={h}
              paragraph={leadership_council.paragraph[i]}
              intro={leadership_council.introduction[i].indexOf("NULL")>=0 ? null : leadership_council.introduction[i]} />
          ))}
        </div>
        {this.sectionIntro(network_councils_intro)}
        <div className="our-funding__council margin-top-25">
          {network_councils.heading.map((h,i)=>(
            <FunderList type="council" columns={2} key={`funder-${i}`}
              heading={h}
              paragraph={network_councils.paragraph[i]}
              intro={network_councils.introduction[i].indexOf("NULL")>=0 ? null : network_councils.introduction[i]} />
          ))}
        </div>
        {this.sectionIntro(program_councils_intro)}
        <div className="our-funding__circle margin-top-25">
          {program_councils.heading.map((h,i)=>(
            <FunderList type="council" columns={2} key={`funder-${i}`}
              heading={h}
              paragraph={program_councils.paragraph[i]}
              intro={program_councils.introduction[i].indexOf("NULL")>=0 ? null : program_councils.introduction[i]} />
          ))}
        </div>
      </section>
    );
  }
}

class OurFundingMain extends Component {
  //https://na-data-projects.s3.amazonaws.com/projects/
  componentDidMount(){
    if(!this.el) return;
    const script = document.createElement("script");

    script.src = `https://na-data-projects.s3.amazonaws.com/projects/${this.props.dataScript}`;
    script.async = true;

    this.el.appendChild(script);
  }
  render(){
    let { data : { how_were_funded, transparency_table, donate_button, charity_navigator } } = this.props;

    return(
      <div class="our-funding-main" ref={(el)=>{ this.el = el; }}>
        <Body data={how_were_funded} aside={<div className="buttons">
          <div className="charity-navigator-img margin-bottom-25">
            {/* <img src={charity_navigator.inline_image[0].url}/> */}
            <img src="https://na-production.s3.amazonaws.com/images/4Star_234x60bw.min-800x800.jpg" style={{width: '100%', maxWidth: '350px', margin: '0 auto', display: 'block'}}/>
          </div>
          <div style={{textAlign: "center"}}>
            <a className="button" href={donate_button.button[0].button_link}>{donate_button.button[0].button_text}</a>
          </div>
        </div>}/>
        <div className="funding-table container--1080">
          <h1>{transparency_table.heading[0]}</h1>
          <h3>{transparency_table.dataviz[0].title}</h3>
          <div className="dataviz__chart-container">
      			<div className="dataviz__chart-area" id={transparency_table.dataviz[0].container_id}></div>
      		</div>
          <div className="margin-top-35 margin-bottom-60" dangerouslySetInnerHTML={{__html: transparency_table.paragraph[0] }} />
        </div>
      </div>
    );
  }
}



export default class OurFunding extends Component {
  findSubpage = (slug) => {
    let { response: { results } } = this.props;
    return results.subpages.find(s=>s.slug===slug);
  }
  render(){
    let { response: { results } } = this.props;
    let donate = this.findSubpage('donate');
    return (
      <div className="home__panels__content">
        <Nav />
        <Route path="/our-funding/" exact render={(props)=>( <OurFundingMain data={results.data} dataScript={results.data_project_external_script}/> )}/>
        <Route path="/our-funding/our-funders/" render={(props)=>( <OurFunderLists data={this.findSubpage('our-funders').data} heading={this.findSubpage('our-funders').title}/> )}/>
        <Route path="/our-funding/corporate-circle/" render={(props)=>( <FunderLists data={this.findSubpage('corporate-circle').data} /> )}/>
        <Route path="/our-funding/new-america-councils/" render={(props)=>( <Councils data={this.findSubpage('new-america-councils').data} /> )}/>
        <Route path="/our-funding/donate/" exact render={(props)=>(
          <div className="container--1080 margin-80">
            <div className="row gutter-20">
              <article className="col-md-7 post-body home__panel__body__text">
              <div className="margin-bottom-35">
                <a className="button" href={donate.data.donate.button[0].button_link}>{donate.data.donate.button[0].button_text}</a>
              </div>
              <div dangerouslySetInnerHTML={{__html: donate.data.donate.paragraph[0] }} />
              </article>
            </div>
          </div>
        )}/>
      </div>
    );
  }
}
        //
        //
