import { Component } from 'react';
import { ImageAside, Reel, Body } from '../components';
import { Route, NavLink } from 'react-router-dom';

class FunderList extends Component {
  parseFunderList = (html, cols=3) => {
    let funders = this.getJSXFromHTML(html);
    let len = Math.ceil(funders.length/cols)-1;

    let groups = [];
    for(let i=0; i<cols; i++){
      let start = len*i + i*1;
      let end = i===cols-1 ? funders.length-1 : len * (i+1) + i;
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
        <label className="block margin-top-0">{f.innerText}</label>
      ));

    return Array.from(funders).map((f,i)=>{
      let b = f.getElementsByTagName('b')[0];
      let name = b.innerText;
      let position = f.innerText.replace(name, '');

      return (
        <div className="our-funding__council-list__item margin-bottom-25">
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
      <div className="home__panel__funders-list margin-bottom-80" >
        <div className="row gutter-20">
          <div className="col-7">
            <h2 className="margin-bottom-25">{heading}</h2>
            <p dangerouslySetInnerHTML={{__html: intro}} />
          </div>
        </div>
        <div className="row gutter-20">
          {groupedLists.map((g,i)=>(
            <div className="col-md-4">
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

class FunderLists extends Component {

  render(){
    let { data : { funders_intro, funders } } = this.props;
    return (
      <section className="funders-list post-body container--1080">
        <div className="row gutter-10">
          <div className="col-md-7">
            <h1 className="margin-top-0">{funders_intro.heading[0]}</h1>
            <p className="margin-bottom-80" dangerouslySetInnerHTML={{__html: funders_intro.paragraph[0] }}/>
          </div>
        </div>
        {funders.heading.map((h,i)=>(
          <FunderList type="funder"
            heading={h}
            paragraph={funders.paragraph[i]}
            intro={funders.introduction[i].indexOf("NULL")>=0 ? null : funders.introduction[i]} />
        ))}
      </section>
    );
  }
}

const NavItem = ({ url, label, exact=false }) => (
  <li>
    <NavLink exact className={`button--text program__nav__link`} to={url}>
      {label}
    </NavLink>
  </li>
);


class Nav extends Component {

  render(){
    return (
      <div className={`container--1080 our-funding__nav margin-top-15`}>
        <ul className="inline">
          <NavItem url={`/our-funding/`} exact={true} label="Gift Guidelines"/>
          <NavItem url={`/our-funding/our-funders/`} label="Funders"/>
          <NavItem url={`/our-funding/circles-and-councils/`} label="Circles and Councils"/>
          <NavItem url={`/our-funding/donate/`} label="Donate"/>
        </ul>
      </div>
    );
  }
}

class CirclesAndCouncils extends Component {
  sectionIntro = (intro) => {
    return (
      <div className="our-funding__intro row gutter-20">
        <div className="col-9">
          <h1 className="margin-top-0 margin-bottom-25">{intro.heading[0]}</h1>
          <p className="margin-top-25 margin-bottom-80" dangerouslySetInnerHTML={{__html: intro.introduction[0] }}/>
        </div>
      </div>
    );
  }
  render(){
    let { data : {
      circles_and_councils_intro,
      councils,
      program_councils_intro,
      program_councils,
      circles_intro,
      circles
    }} = this.props;
    return (
      <section className="container--1080 our-funding__circles_and_councils">
        {this.sectionIntro(circles_and_councils_intro)}
        <div className="our-funding__council">
          {councils.heading.map((h,i)=>(
            <FunderList type="council" columns={2}
              heading={h}
              paragraph={councils.paragraph[i]}
              intro={councils.introduction[i].indexOf("NULL")>=0 ? null : councils.introduction[i]} />
          ))}
        </div>
        {this.sectionIntro(program_councils_intro)}
        <div className="our-funding__council margin-top-25">
          {program_councils.heading.map((h,i)=>(
            <FunderList type="council" columns={2}
              heading={h}
              paragraph={program_councils.paragraph[i]}
              intro={program_councils.introduction[i].indexOf("NULL")>=0 ? null : program_councils.introduction[i]} />
          ))}
        </div>
        {this.sectionIntro(circles_intro)}
        <div className="our-funding__circle margin-top-25">
          {circles.heading.map((h,i)=>(
            <FunderList type="funder" columns={2}
              heading={h}
              paragraph={circles.paragraph[i]}
              intro={circles.introduction[i].indexOf("NULL")>=0 ? null : circles.introduction[i]} />
          ))}
        </div>
      </section>
    );
  }
}



export default class OurFunding extends Component {

  render(){
    let { response: { results : { data } } } = this.props;
    let frame = data.donate.iframe[0];
    return (
      <div className="home__panels__content">
        <Nav />
        <Route path="/our-funding/" exact render={(props)=>( <Body data={data.gift_guidelines} /> )}/>
        <Route path="/our-funding/our-funders/" render={(props)=>( <FunderLists data={data} /> )}/>
        <Route path="/our-funding/circles-and-councils/" render={(props)=>( <CirclesAndCouncils data={data} /> )}/>
        <Route path="/our-funding/donate/" exact render={(props)=>(
          <Body data={data.donate}><iframe src={frame.source_url} width="100%" height="1200" /></Body>
        )}/>
      </div>
    );
  }
}
        //
        //
