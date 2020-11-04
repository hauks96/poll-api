# Authentication Package Integration
The following is documentation and instructions on usage of this authentication package.
To integrate the authentication, import the Auth package into your project and use the methods described below.
The error messages in this package give a clear explanation of what went wrong and are recomended to use as feedback to users.

#### login
Logs in a user.\
Takes arguments:
- `username: str`
- `password: str`

This method throws AuthenticationFailed if the login failed.

#### logout
Logs out a user that is currently logged in. Does nothing if not logged in.

#### createUser
Create a new user. Takes a `dictionary` as argument. Must contain following attributes/keys:
- `username`: string of length at least 5
- `password`: string of length at least 5
- `firstName`: string
- `lastName`: string
- `regionID`: string decimal
- `ssn`: string decimal and length at least 8. Unique to each user

Raises InvalidUserCreation if anything goes wrong.

#### removeAccount
Removes the users account. User must be logged in to use this method.\
Takes arguments:
- `username: str`
- `password: str`

Raises AuthenticationFailed if method was invalid.

#### user_region
Returns the users registered region id.
- `no parameters`

Raises AuthenticationFailed if user is not authenticated.

#### user_creations
Fetches and returns all the users creations of a specific data type. Takes as arguments `the class of the interface calling the method`.\
Raises AuthenticationFailed if user is not authenticated.

#### authorize_modification
Checks if the user is authorized to modify an object related to the current interface.\
Takes arguments:
- `Interface class`: The class of the interface calling the method
- `model id`: The integer ID of the data model that the user wants to modify

Raises AuthenticationFailed if user is not authenticated or authorized for the operation in question.

#### create_auth_relation
Creates a relationship between the data object related to the current interface and the user. Method should be used AFTER an object has been successfully created by user.\
Takes arguments:
- `Interface class`: The class of the interface calling the method
- `model id`: The integer ID of the data model that the user wants to modify

Raises AuthenticationFailed if user is not authenticated.\
Raises AuthRelationCreationFailed if the creation was illegal.\
Raises CreationLimitReached if the user has reached the creation limit of this type of data.

#### remove_auth_relation
Deletes a relationship between a model and it's creator.\
Takes arguments:
- `Interface class`: The class of the interface calling the method
- `model id`: The integer ID of the data model that the user wants to modify

Raises AuthenticationFailed if not authorized.\
Raises AuthRelationDeletionFailed if relationship doesn't exist.


# Security Evaluation
| Asset | Value | Risk | Probability | Exposure | Control |
|----|----|----|----|----|----|
| Created data | Medium | Unauthorized person modifies or removes the data that someone else created. | High | High | Create authentication system that stores relations between users and created information. |
| User private information | High | Information gets leaked | Low | High | Store users login credentials separate from users private information and make sure the information is unreachable |
| User login credentials | High | Users credentials get stolen | Medium | High | Make sure the user credentials are not required for every authentication requiring request. Store the credentials encoded. Make the credentials unreachable after login. |
| Server storage | Very High | Someone tries to overflow our database or crash our server with creating extreme amounts of new data | Very High | Low | Make sure that every authenticated user has a limited amount of creations available to them for every datamodel |

## Security Features 
The implemented security features of the authentication system

#### Component
The authentication system is an individual compoment. It is integrated in the main software as a completely separate entity using the authentication systems API interface. _No backend models were modified in the original project to implement the relations_.

#### Encoded login credentials
The users credentials are hashed using the industry standard sha256 as soon as a user has logged in. `sha256 (usn+pw)`

#### Unreachable user data
All user information is unreachable from outside the authentication package. The only retrievable information is the user's region.

#### Sensitive user information stored separately
All personal information on users is stored separately form the user login credentials and is not reachable after creation.

#### Vote choices not stored in users creation data
To eliminate the leaking of users vote choices, the authentication system does not store the users vote choice but only what poll he voted on.

#### Limited creation
Every user has limited amount of creations available of each datatype to eliminate database over-population.
