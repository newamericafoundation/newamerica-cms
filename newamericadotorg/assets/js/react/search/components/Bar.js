import { Component } from 'react';
import { NAME } from '../constants';

export default class Bar extends Component {
  timeout = 0
  constructor(props){
    super(props);
    let { page, setQueryParam } = this.props;
    let value = '';
    if(page=='search-page'){
      let params = new URLSearchParams(window.location.search);
      let query = params.get('query');
      if(query){
        value = query;
        setQueryParam('query', value, true);
      }
    }

    this.state = { value };
  }
  change = (e) => {
    this.setState({ value: e.target.value });
  }

  componentWillUpdate(nextProps, nextState){
    if(this.state.value == nextState.value) return;
    clearTimeout(this.timeout);
    this.timeout = setTimeout(()=>{
      this.props.setQuery({
        query: nextState.value,
        page: 1
      }, true);
      if(this.props.page=='search-page'){
        let url = `${window.location.origin}${window.location.pathname}?query=${nextState.value}`;
        window.history.replaceState(null, null, url);
      }
    }, 500);
  }

  componentDidMount() {
    this.el.focus();
  }

  render(){
    return (
      <div className="search__bar">
        <input value={this.state.value}
          type="text"
          ref={(el)=>{this.el = el;}}
          autofocus={true}
          placeholder="Search names or keywords"
          onChange={this.change} />
      </div>
    );
  }
}
