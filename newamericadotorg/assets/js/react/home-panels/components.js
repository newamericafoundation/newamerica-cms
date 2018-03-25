import { Component } from 'react';
import { NavLink } from 'react-router-dom';

export const NavItem = ({ url, label, exact=false }) => (
  <li>
    <label className="button--text link">
      <NavLink exact className={`button--text program__nav__link`} to={url}>
        {label}
      </NavLink>
    </label>
  </li>
);


class Panel extends Component {
  parseHTMLText = (html) => {
    let div = document.createElement('div');
    div.innerHTML = html;
    return div.innerText;
  }
}

export class ImageAside extends Panel {
  render(){
    let { data, grayscale } = this.props;
    return (
      <section className="home__panel__image-aside scroll-target" data-scroll-trigger-point="bottom" data-scroll-offset="35vh">
        <div className="container--1080">
          <div className="row gutter-20">
            <div className="col-md-6 home__panel__image-aside__image margin-bottom-35">
              <img src={data.inline_image[0].url} className={`${grayscale ? 'grayscale' : ''}`} />
            </div>
            <div className="col-md-5 push-md-1 home__panel__image-aside__text" >
              <div className="home__panel__image-aside__text__wrapper">
                <h1 className="margin-top-0 margin-bottom-25">{data.heading[0]}</h1>
                <p className="margin-bottom-0 margin-top-25">
                  {this.parseHTMLText(data.introduction[0])}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export class Reel extends Panel {

  constructor(props){
    super(props);
    let { data } = props;
    this.state = {
      len: data.paragraph.length+1,
      index: -1,
      pause: false
    }
  }

  componentDidMount(){
    this.nextFrame();
    this.play();
  }

  play = () => {
    setInterval(()=>{
      this.nextFrame();
    }, this.props.interval)
  }

  pause = () => {
    setTimeout(()=>{
      this.setState({
        pause: true,
        index: 0
      });
    }, 1200);

    setTimeout(()=>{
      this.setState({
        pause: false
      });
    }, 1500);
  }

  nextFrame = () => {
    let { len, index, offset } = this.state;
    let { data } = this.props;
    if(index >= len-2) this.pause();

    if(index >= len-1) index = 0;
    else index += 1;

    this.setState({
      index
    });
  }

  reelContent = (p,i) => {
    let { setHTML, data } = this.props;
    let { index } = this.state;
    if(setHTML)
      return (
        <div className={`home__reel__frame ${index===i ? 'active' : ''}`} key={`frame-${i}`}>
          <div className="home__reel__frame__wrapper" dangerouslySetInnerHTML={{__html: p }} />
        </div>
      );

    return (
      <div className={`home__reel__frame ${index===i ? 'active' : ''}`} key={`frame-${i}`}>
        <h1 className="margin-0">{this.parseHTMLText(p)}</h1>
      </div>
    );
  }

  render(){
    let { data,  } = this.props;
    let { index, pause, len} = this.state;
    return (
      <section className="home__panel__promo scroll-target" data-scroll-trigger-point="bottom" data-scroll-offset="35vh">
        <div className="container--1080">
          <div className={`row gutter-20 home__reel`}>
            <div className="col-md-6">
              <div className="home__panel__promo__text">
                <h1 className="promo margin-top-0 margin-bottom-15">{data.heading[0]}</h1>
                <p className="margin-bottom-35 margin-top-15">{this.parseHTMLText(data.introduction[0])}</p>
              </div>
            </div>
            <div className="col-md-5 push-md-1">
              <div className={`home__reel__frames ${pause ? 'pause' : ''}`} style={{top: `${-index * 100}%`}}>
                {data.paragraph.map((p,i)=>(
                  this.reelContent(p,i)
                ))}
                {this.reelContent(data.paragraph[0], len-1)}
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export class Body extends Panel {
  render(){
    let { data } = this.props;

    return (
      <section className="home__panel__body">
        <div className="container--1080">
          <div className="row gutter-20">
            <article className="col-md-7 post-body home__panel__body__text">
              {data.heading.map((h,i)=>(
                <div className="" key={`heading-${i}`}>
                  <h1 className="margin-top-0">{data.heading[i]}</h1>
                  <p dangerouslySetInnerHTML={{__html: data.paragraph[i]}} />
                  {this.props.children}
                </div>
              ))}
            </article>
            {data.resource_kit &&
            <div className="col-md-4 push-md-1 home__panel__body__aside">
              <div className="aside">
                <label className="block bold margin-top-0">{data.resource_kit[0].title}</label>
                <label className="block margin-bottom-25">{data.resource_kit[0].description}</label>
                {data.resource_kit[0].resources.map((r,i)=>(
                  <div className="aside__item" key={`resource-${i}`}>
                    <h3><a>{r.value.name}</a></h3>
                    {r.value.description && <label className="block">{this.parseHTMLText(r.value.description)}</label>}
                  </div>
                ))}
              </div>
            </div>}
          </div>
        </div>
      </section>
    );
  }
}
