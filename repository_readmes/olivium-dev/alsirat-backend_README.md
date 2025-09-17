# README for olivium-dev/alsirat-backend

## Getting Started

### Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).

## Architecture overview

This application is at server side. The architecture proposes a function oriented architecture implementation with multiple autonomous AWS Lambdas that are exposed by an AWS API Gateway. All Endpoints are secured by JWT Tokens.

There are three key projects under src folder:
- Api: contains web api controllers used for local development, generating Swagger Docs, and making local http requests.
- Application: contains services, models and repositories.
- Lambda: contains projects used for exposing services through AWS lambdas.

### Tests

All test projects are under tests folder. Tools: xUnit.net and Moq.

### Application

We organize Services by workflows and data models. A repository can be created for each data model.

#### Steps to create a Service

1. Create an interface and its methods' signatures. Name it nameOfService + Service, like ITemplateService.
2. Create a class to implement this interface. You can add a reference to any repository you need to.
3. A Service must have its depencies inject on its constructor so it can be tested in isolation.
7. Please write your tests in tests/Application/nameOfServiceTest.cs. Name it nameOfService + Test.

#### Steps to create a Repository

All queries to the database are handled by Dapper. Mores details at https://github.com/StackExchange/Dapper/tree/master/Dapper.Contrib.

1. Create an interface and its methods' signatures. Name it nameOfRepository + Repository, like IRepository.
2. Create a class to implement this interface. Check TemplateRepository.cs for an example. Please, use Dapper to run your queries.

Here's some examples:
* SELECT
  * var car = connection.Get<Car>(1);
  * var cars = connection.GetAll<Car>();
* INSERT
  * connection.Insert(new Car { Name = "Volvo" });
  * connection.Insert(cars);
* UPDATE
  * connection.Update(new Car() { Id = 1, Name = "Saab" });
  * connection.Update(cars);
* DELETE
  * connection.Delete(new Car() { Id = 1 });
  * connection.Delete(cars);
  * connection.DeleteAll<Car>();

### Lambda

A AWS lambda is a serverless function that responds to events, like a HTTP request.
We organize lambdas by workflows or data models, and group functions related to those workflows and data models together in the Lambda.
Deploys are handled by the Serverless Framework (serverless.com) which reads the file serverless.yml and creates all AWS resources required to run each AWS Lambda.

#### Steps to create a Lambda

1. Come up with a name for this new Lambda. It's common to use a noun.
2. Duplicate the folder src/Lambda/Template. Rename this folder to its new name.
3. Open the file aws-csharp.csproj and change AssemblyName from Lambda to its new name.
4. Rename the file aws-csharp.csproj to newLambdaNameHere.csproj.
5. Open the file Handler.cs. Change namespace to its new name. No need to change the class name. Each new method created should resemble the Hello method. You should consider creating all business logic inside a Service at Application/Services.
6. Open the file serverless.yml and change service from template to its new name. You'll also have to create a new function here for each one of your Handler.cs file.
7. Please write your tests in tests/Lambda/NewLambaNameHereTest.cs

### Api

#### Steps to create a Controller

1. Duplicate the file TemplateController.cs and give it a new name.
2. Open this new file and change all occurrences of TemplateController to its new name.
3. You can inject any required services through its constructor.
4. For every new Service required by a controller it has to be registered at the file Startup.cs by using the method services.AddScoped like services.AddScoped<ITemplateService, TemplateService>();

## Swagger Documentation

1. Copy the contents of docs/swagger.json
2. Open https://editor.swagger.io and paste it there.

## Environment variables

| Variable                                | Description         |
| -------------                           |-------------|
| AWS_DEV_LAMBDA_KEY                      | AWS Key used for development stage deploys|
| AWS_DEV_LAMBDA_SECRET                   | AWS Secret used for development stage deploys|
| AWS_PROD_LAMBDA_KEY                     | AWS Key used for production stage deploys|
| AWS_PROD_LAMBDA_SECRET                  | AWS Secret used for production stage deploys|
| AWS__S3__Region                         | AWS Region for S3 storage
| AWS__S3__AcessKey                       | AWS Key used for S3 integration
| AWS__S3__SecretAcessKey                 | AWS Secrete used for S3 integration
| AWS__S3__BookBucketName                 | AWS Bucket used for storing Books
| AWS__S3__ImageBucketName                | AWS Bucket used for storing Images
| ConnectionStrings__AppConnectionString  | Application connection string used for PosgreSQL|
| Db__Username                            | PostgreSQL user|
| Db__Password                            | PostgreSQL password|
| JWT__IssuerSigningKey                   | Signing key used for validading and creating JWT tokens
| JWT__ExpirationInSeconds                | JWT lifetime in seconds
| Algolia__ApplicationId                  | Application Id used for integrating Algolia with our backend
| Algolia__ApiKey                         | Api Key used for integrating Algolia with our backend
| Algolia__IndexName                      | Search Index Name used for integrating Algolia with our backend (Quran Index)
| Algolia__AhadithIndexName               | Search Index Name used for integrating Algolia with our backend (Ahadith Index)
| ANDROID_API_KEY                         | Api Key used from Android app for creating JWT tokens
| APPLE_API_KEY                           | Api Key used from Apple app for creating JWT tokens
| Gold__Api__ApiKey                       | Api Key for https://www.goldapi.io

## Database / Patching

Any change to database Data or Schema has to be made through a script named patch.sql present on the root of this project. The script is incremental so that all changes will run and  be applied to the database if needed to. Please note that if you are sure about updating your local database then you should comment the last line and uncomment the previous line in order to COMMIT all changes.

### Database connection string

#### Offline
```sh
ConnectionStrings__AppConnectionString = "Data Source=.;Initial Catalog=alsirat;Integrated Security=True;"
```

#### Online
```sh
ConnectionStrings__AppConnectionString = "Server=alsirat-prod.c2uq44ejmiik.us-east-1.rds.amazonaws.com;Database=postgres;Port=5432;SSL Mode=Require;Trust Server Certificate=true;"
```

## Steps to Build / Run / Test from source

To build you can use the standard dotnet cli stool:
```sh
dotnet build
```

#### Running api
```sh
dotnet run --project src/Api
```

#### Running Unit Tests
```sh
dotnet test tests/Api
dotnet test tests/Application
dotnet test tests/Lambda.Tests
```
