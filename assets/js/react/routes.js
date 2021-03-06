import React from 'react';
import {Route, IndexRoute} from 'react-router';
import { sessionService } from 'redux-react-session';

import App from './components/app';
import UsersNew from './containers/users_new';
import SessionsNew from './containers/sessions_new';
import Home from './containers/home'
import Profile from './containers/profile'
import TasksNew from './containers/new_task'
import TasksEdit from './containers/edit_task'
import StriveStore from './containers/strive_store'
import ProfilePicturePicker from './containers/profile_picture_picker'
import SearchResults from './containers/search_results'
import StoreNew from './containers/store_new'
import StoreIndex from './containers/store_index'

export default (
  <Route path='/' component={App}>
    <IndexRoute component={SessionsNew} />
    <Route path='register' component={UsersNew} />
    <Route path='home' component={Home} />
    <Route path='profile/:id' component={Profile} />
    <Route path='tasks/new' component={TasksNew} />
    <Route path='tasks/edit' component={TasksEdit} />
    <Route path='store' component={StriveStore} >
      <IndexRoute component={StoreIndex} />
      <Route path='new' component={StoreNew} />
    </Route>
    <Route path='pictures' component={ProfilePicturePicker} />
    <Route path='search_results' component={SearchResults} />
  </Route>
);
