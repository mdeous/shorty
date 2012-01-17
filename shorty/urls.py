# -*- coding: utf-8 -*-
#    This file is part of Shorty.
#
#    Shorty is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Shorty is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Shorty.  If not, see <http://www.gnu.org/licenses/>.

from shorty.views.frontend import frontend, IndexView, ShortLinkRedirectView
from shorty.views.users import users, LoginView, RegisterView, LogoutView

routes = [
    ((frontend, ''),
        ('/', IndexView.as_view('index')),
        ('/<short_code>', ShortLinkRedirectView.as_view('redir')),
    ),
    ((users, '/user'),
        ('/login', LoginView.as_view('login')),
        ('/logout', LogoutView.as_view('logout')),
        ('/register', RegisterView.as_view('register')),
    ),
]
