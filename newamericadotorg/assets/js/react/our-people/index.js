import { BrowserRouter } from 'react-router-dom';
import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME, ID } from './constants';
import { Routes } from './components/Routes';
import PeopleList from './components/PeopleList';

class APP extends Component {
  render(){
    return (
      <BrowserRouter>
        <section className="our-people">
          <Routes />
          <PeopleList />
        </section>
      </BrowserRouter>
    );
  }
}


export default { APP, NAME, ID };
