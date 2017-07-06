import { Component } from 'react';
import { Fetch } from '../../components/API';
import { NAME } from '../constants';

class Bar extends Component {
  timeout = 0
  constructor(props){
    super(props);
    this.state = { value: '' };
  }
  change = (e) => {
    this.setState({ value: e.target.value });
  }

  componentWillUpdate(nextProps, nextState){
    if(this.state.value == nextState.value) return;
    clearTimeout(this.timeout);
    this.timeout = setTimeout(()=>{
      this.props.setQueryParam('query', nextState.value, true);
    }, 500);
  }

  render(){
    return (
      <div className="search__bar">
        <input value={this.state.value} onChange={this.change} />
      </div>
    );
  }
}

const BarWrapper = () => (
  <Fetch
    endpoint={'search'}
    name={NAME}
    fetchOnMount={false}
    eager={false}
    component={Bar} />
);

export default BarWrapper;
