import { Component } from 'react';
import { PlusX } from '../components/Icons';


const NAME = 'resourcesBlock';
const ID = 'resources-block';

class ResourceItem extends Component {

  render(){
    let { resource, type } = this.props;
    return (
      <div className="resources-block__item-wrapper col-lg-4 col-md-6 col-12">
        <div className="resources-block__item">
          <div className="resources-block__item__top">
            <div className="resources-block__item__top__heading">
              <label className="block bold">{resource.name}</label>
              {type=='person' && <label className="block caption">{resource.title}</label>}
            </div>
            {resource.image &&
              <div className="resources-block__item__top__image">
                <img src={resource.image} />
              </div>}
          </div>
          <div className="resources-block__item__bottom">
            <div className="resources-block__item__bottom__buttons">
              {resource.description &&
                <div className="resources-block__item__bottom__buttons__button">
                  <PlusX x={false} />
                </div>
              }
            </div>
          </div>
        </div>
      </div>
    );
  }
}


class APP extends Component {

  render(){
    let { resources } = this.props;
    if(!resources) return null;
    resources = JSON.parse(resources);
    console.log(resources);
    return (
      <div className="resources-block row">
        {resources.map((r,i)=>(
          <ResourceItem resource={r} key={`resource-${i}`}/>
        ))}
      </div>
    );

  }
}



export default { APP, NAME, ID, MULTI: true };
