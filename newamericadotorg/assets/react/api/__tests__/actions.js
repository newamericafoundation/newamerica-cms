import MockStore from 'redux-mock-store';
import thunk from 'redux-thunk';

const mockStore = MockStore([thunk]);

import { fetchData } from '../actions';

let fakeState = {
  fakeComponent: {
    params: {
      baseUrl: 'https://fake.io/api/',
      endpoint: '',
      query: {}
    }
  }
}

const mockResponse = (status, statusText, response) => {
  return new window.Response(response, {
    status: status,
    statusText: statusText,
    headers: {
      'Content-type': 'application/json'
    }
  });
};

describe('fetching data from napi', () => {

  beforeEach(()=>{
    window.user = {};
  });

  test('calls napi endpoint and dispatches proper variables on success', () => {
    window.fetch = jest.fn().mockImplementation(() =>
      Promise.resolve(mockResponse(200, null, JSON.stringify({
        count: 1,
        results: []
      }))
    ));

    const store = mockStore(fakeState);

    let expectedActions = [
      "SET_FETCHING_STATUS",
      "SITE_IS_LOADING",
      "SITE_IS_LOADING",
      "SET_RESPONSE"
    ];

    return store.dispatch(fetchData('fakeComponent'))
      .then(() => {
        const actualActions = store.getActions().map(action => action.type);
        expect(actualActions).toEqual(expectedActions)
     });

  });

});
