# QSteroids

This a tool for providing improvements on code performances of Qt codes.

## Documentation
Currently the this script can inject property code and the debbuging using the Other debugging techniques: <https://developer.blackberry.com/cascades/documentation/getting_started/tools/debugging.html>
#### Q\_SETEROID\_PROPERTY(  _[Type]_ _[propertyName]_ ,  _[r]__[w]__[n]__[f]_  )
This command can be used for inject Q\_PROPERTY code.

* **Type:** This field is the type of the property. You must to include manually the if it is not included yet;
* **propertyName:** here you have to put the property name. It is evaluated with the same C++ name rules;
* **r:** if it appears the read method for the property will be injected;
* **w:** if it appears the write method for the property will be injected;
* **n:** if it appears the propertyNameChanged signal for the property will be injected;
* **f:** if it appears the FINAL flag will be injected at the property declaration;

> **Example**
>
> Q\_STEROID\_PROPERTY(QString name, rwn)

Step by step how to use this:

1. You have to download the script to the PATH_YOU_WANT;
2. You need to add the follow command to the .pro file: ```system(c:\\Users\\rsarmentopeixoto\\Dev\\QSteroids\\qsteroids.py)```
3. You need to add the Q_STEROID_PROPERTY at the hpp file. There is no specific location for this. This is visually better bellow the Q_OBJECT keyword; 
4. Now you just need to build the project on momentics;
5. After building, the generated code is named with the _qsteroided word;
6. Check the new file. If it is correct, delete the original and then remove the _qsteroided from the file name;
7. If you need to rerun the generation you need to remove the _qsteroided file. 

### Known limitations
The signals, private, public slots need to be in the following sequence:

* ```signals:```
* ```public slots:```
* ```private:```

##### Before the injection
This is the code before the injection. You only need to add the QSteroid properties and than run the script.

**helloworld.hpp**
	
	#ifndef HELLOWORLD_H_
	#define HELLOWORLD_H_

	#include <bb/cascades/GroupDataModel>

	class HelloWorld : public QObject
	{
		Q_OBJECT
		Q_STEROID_PROPERTY(QString name, rwn)
		Q_STEROID_PROPERTY(bb::cascades::GroupDataModel * gmodel, rnf)
		Q_STEROID_PROPERTY(int a, nwr)
		Q_STEROID_PROPERTY(QList<QObject*> model, rwnf)
	public:
		HelloWorld();
		virtual ~HelloWorld();
	};

	#endif /* HELLOWORLD_H_ */

**helloworld.cpp**
	
	#include "HelloWorld.h"

	HelloWorld::HelloWorld() {
	}

	HelloWorld::~HelloWorld() {
	}

##### After the injection

**helloworld.hpp**

	#ifndef HELLOWORLD_H_
	#define HELLOWORLD_H_

	#include <bb/cascades/GroupDataModel>

	class HelloWorld : public QObject
	{
		Q_OBJECT
		Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
		Q_PROPERTY(bb::cascades::GroupDataModel * gmodel READ gmodel NOTIFY gmodelChanged FINAL)
		Q_PROPERTY(int a READ a WRITE setA NOTIFY aChanged)
		Q_PROPERTY(QList<QObject*> model READ model WRITE setModel NOTIFY modelChanged FINAL)
	public:
		HelloWorld();
		Q_INVOKABLE QString name();
		Q_INVOKABLE void setName(QString newName);
		Q_INVOKABLE bb::cascades::GroupDataModel * gmodel();
		Q_INVOKABLE void setGmodel(bb::cascades::GroupDataModel * newGmodel);
		Q_INVOKABLE int a();
		Q_INVOKABLE void setA(int newA);
		Q_INVOKABLE QList<QObject*> model();
		Q_INVOKABLE void setModel(QList<QObject*> newModel);
	signals:
		void nameChanged();
		void gmodelChanged();
		void aChanged();
		void modelChanged();
		virtual ~HelloWorld();
	private:
		QString m_name;
		bb::cascades::GroupDataModel * m_gmodel;
		int m_a;
		QList<QObject*> m_model;
	};

	#endif /* HELLOWORLD_H_ */

**helloworld.cpp**

	#include "HelloWorld.h"
	HelloWorld::HelloWorld() {
	}

	HelloWorld::~HelloWorld() {
	}

	QString HelloWorld::name() {
		return m_name;
	}
	void HelloWorld::setName(QString newName){
		if(m_name != newName)
			m_name = newName;
			emit nameChanged();
	}
	bb::cascades::GroupDataModel * HelloWorld::gmodel() {
		return m_gmodel;
	}
	void HelloWorld::setGmodel(bb::cascades::GroupDataModel * newGmodel){
		if(m_gmodel != newGmodel)
			m_gmodel = newGmodel;
			emit gmodelChanged();
	}
	int HelloWorld::a() {
		return m_a;
	}
	void HelloWorld::setA(int newA){
		if(m_a != newA)
			m_a = newA;
			emit aChanged();
	}
	QList<QObject*> HelloWorld::model() {
		return m_model;
	}
	void HelloWorld::setModel(QList<QObject*> newModel){
		if(m_model != newModel)
			m_model = newModel;
			emit modelChanged();
	}

	
### Q\_STEROID\_DEBUG
It's not implented yet.