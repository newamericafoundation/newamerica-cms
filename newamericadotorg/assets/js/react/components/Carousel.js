import { Component } from 'react';

class Carousel extends Component {
  static propTypes = {
    items: PropTypes.array.isRequired,
    n: PropTypes.number,
    itemComponent: PropTypes.func
  }

  static defaultProps = {
    n: 6,
    itemComponent: () => (<div></div>)
  }

  itemGroups = [];
  hasNext = false;
  hasPrevious = false;

  constructor(props){
    super(props);
    this.state = {
      position: 0
    }
  }

  updateState = (props, state) => {
    let { position } = state;
    this.itemGroups = this.splitItems(props.items);
    this.hasNext = position < this.itemGroups.length-1;
    this.hasPrevious = position > 0;
  }

  componentWillMount(){
    this.updateState(this.props, this.state);
  }

  componentWillUpdate(nextProps, nextState){
    this.updateState(nextProps, nextState);
  }

  slideRight = () => {
    let { position } = this.state;
    if(!this.hasNext) return;
    this.setState({
      position: position+1
    });
  }

  slideLeft = () => {
    let { position } = this.state;
    if(!this.hasPrevious) return;
    this.setState({
      position: position-1
    });
  }

  splitItems = (items) => {
    if(!items) return [];
    let { n } = this.props;
    let splitItems = [];
    for (let i=0; i<items.length; i+=n)
        splitItems.push(items.slice(i,i+n));
    return splitItems;
  }

  render() {
    let { n } = this.props;
    let col = Math.floor(12/n);

    return (
      <div className="carousel container" >
        <div className="carousel__group-wrapper">
        {this.hasPrevious&&<div className="carousel__left-arrow" onClick={this.slideLeft}/>}
        {this.itemGroups.map((g,i)=>(
          <div className="carousel__group" style={{ left: `-${this.state.position*100}%`}}>
            <div className="row carousel__goup__items gutter-10">
            {g.map((item, j)=>(
              <div className={`carousel__group__item col-${col}`}>
                <this.props.itemComponent item={item} />
              </div>
            ))}
            </div>
          </div>
        ))}
        {this.hasNext&&<div className="carousel__right-arrow" onClick={this.slideRight}/>}
        </div>
      </div>
    );
  }
}

export default Carousel;
