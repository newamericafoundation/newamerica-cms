import { Component } from 'react';
import { PlusX } from '../components/Icons';
import { connect } from 'react-redux';

const NAME = 'resourcesBlock';
const ID = 'resources-block';

class ResourceItem extends Component {

  getRect = () => {
    if(!this.el) return {};
    let top, left, width
    let windowWidth = window.innerWidth;
    let rect = this.el.getBoundingClientRect();
    let parent = this.el.parentNode.parentNode;

    if(windowWidth<992){
      width = '100vw';
      top = 50 - rect.top;
      left = 0 - rect.left + 5;
    } else {
      width = '300%';
      top = 200 - rect.top;
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
              <label className="block bold centered margin-top-0">{resource.name}</label>
              {type=='person' && <label className="block caption centered">{resource.title}</label>}
            </div>
            {resource.image &&
              <div className="resources-block__item__top__image">
                <img src={resource.image} />
              </div>}
            {resource.description &&
              <div className="resources-block__item__top__description post-body">
                <div dangerouslySetInnerHTML={{ __html: resource.description.slice(1,-1)}} />
              </div>}
          </div>
          <div className="resources-block__item__bottom">
            <div className="resources-block__item__bottom__buttons">
              {resource.description &&
                <div className="resources-block__item__bottom__buttons__button" onClick={()=>{expand(index)}}>
                  <PlusX x={expanded} />
                </div>
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


class APP extends Component {
  state = { expanded: false }
  expand = (resourceIndex) => {
    if(this.state.expanded === resourceIndex ) this.setState({ expanded: false });
    else
      this.setState({ expanded: resourceIndex });
  }
  render(){
    let { resources, type } = this.props;
    if(!resources) return null;
    resources = JSON.parse(resources);
    return (
      <div className={`resources-block row gutter-10 ${this.state.expanded !== false ? 'expanded' : ''}`}>
        <div className="resources-block__overlay" onClick={()=>{this.expand(this.state.expanded)}}/>
        {resources.map((r,i)=>(
          <ResourceItem resource={r} type={type} key={`resource-${i}`} index={i} expanded={this.state.expanded===i} expand={this.expand}/>
        ))}
      </div>
    );

  }
}



export default { APP, NAME, ID, MULTI: true };
