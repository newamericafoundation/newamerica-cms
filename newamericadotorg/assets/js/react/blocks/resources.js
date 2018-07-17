import { Component } from 'react';
import { PlusX, Arrow } from '../components/Icons';
import { connect } from 'react-redux';

export const NAME = 'resourcesBlock';
export const ID = 'resources-block';

class ResourceItem extends Component {

  getRect = () => {
    if(!this.el) return {};
    let top, left, width
    let windowWidth = window.innerWidth;
    let windowHeight = window.innerHeight;
    let rect = this.el.getBoundingClientRect();
    let parent = this.el.parentNode.parentNode;

    top = windowHeight * .05 - rect.top;

    if(windowWidth<992){
      width = '100vw';
      left = 0 - rect.left + 5;
    } else {
      width = '300%';
      left = parent.getBoundingClientRect().left - rect.left + 10;
    }

    return { top, left, width };
  }
  render(){
    let { resource, type, expanded, expand, index } = this.props;
    let rect = this.getRect();

    return (
      <div className="resources-block__item-wrapper col-lg-4 col-md-6 col-12">
        <div className={`resources-block__item ${expanded ? 'open' : ''}`} style={expanded ? rect : {}} ref={(el)=>{this.el=el;}}>
          <div className="resources-block__item__top">
            <div className="resources-block__item__top__heading">
              <h4 className="centered margin-top-0">{resource.name}</h4>
              {type=='person' && <h4 className="caption centered">{resource.title}</h4>}
            </div>
            {resource.image &&
              <div className="resources-block__item__top__image">
                <img src={resource.image} />
              </div>}
            {resource.description &&
              <div className={`resources-block__item__top__description post-body ${!resource.image ? 'no-image' : ''}`}>
                <div dangerouslySetInnerHTML={{ __html: resource.description}} />
              </div>}
          </div>
          <div className="resources-block__item__bottom">
            <div className="resources-block__item__bottom__buttons">
              {resource.description &&
                <div className="resources-block__item__bottom__buttons__button expand" onClick={()=>{expand(index)}}>
                  <PlusX x={expanded} />
                </div>
              }{resource.url &&
                <a href={resource.url} className="resources-block__item__bottom__buttons__button link">
                  <Arrow direction="right" />
                </a>
              }
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// const mapStateToProps = (state) => ({
//   scrollPosition: state.site.scroll.position
// });
//
// ResourceItem  = connect(mapStateToProps)(ResourceItem);


export class APP extends Component {
  state = { expanded: false }
  expand = (resourceIndex) => {
    if(this.state.expanded === resourceIndex ) this.setState({ expanded: false });
    else
      this.setState({ expanded: resourceIndex });
  }
  render(){
    let { resources, type, title, description } = this.props;
    if(!resources) return null;
    resources = JSON.parse(resources);
    return (
      <div className={`resources-block row gutter-10 ${this.state.expanded !== false ? 'expanded' : ''}`}>
        <div className="resources-block__overlay" onClick={()=>{this.expand(this.state.expanded)}}/>
        {title && <div className="resources-block__title col-12 margin-bottom-60">
          <h1 className="centered">{title}</h1>
          <p className="centered">{description}</p>
        </div>}
        {resources.map((r,i)=>(
          <ResourceItem resource={r} type={type} key={`resource-${i}`} index={i} expanded={this.state.expanded===i} expand={this.expand}/>
        ))}
      </div>
    );

  }
}



export default { APP, NAME, ID, MULTI: true };
