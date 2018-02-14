import { Component } from 'react';
import { PublicationsList, PublicationListItem, FilterGroup } from '../../components/Publications';
import { Person } from '../../components/People';
import { Fetch } from '../../components/API';
import { NAME } from '../constants';


export default class Search extends Component {
  timeout = 0;
  constructor(props){
    super(props);
    let { location } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let query = params.get('query');
    this.state = { query }
  }

  change = (e) => {
    clearTimeout(this.timeout);
    this.setState({ query: e.target.value })
    this.timeout = setTimeout(()=>{
      let { history, location } = this.props;
      let params = new URLSearchParams(location.search.replace('?', ''));
      params.set('query', this.state.query);
      history.push(`/search/?${params.toString()}`)
    }, 1000 );
  }
  render(){
    let params = new URLSearchParams(location.search.replace('?', ''));

    return (
      <div className="home__panels__search container">
        <div className="input margin-bottom-35">
          <input type="text" required value={this.state.query} onChange={this.change}/>
          <label className="button--text input__label">Search</label>
        </div>
        {this.state.query &&
        <Fetch name={NAME} endpoint={"search"}
            component={PublicationsList}
            fetchOnMount={true}
            eager={true}
            initialQuery={{
              page_size: 8,
              type: params.get('type'),
              query: params.get('query')
            }}/>}
      </div>
    );
  }
}
