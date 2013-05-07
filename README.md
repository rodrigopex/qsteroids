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

``` Q_STEROID_PROPERTY(QString name, rwn)

Example:
	
	#ifndef ApplicationUI_HPP_
	#define ApplicationUI_HPP_

	#include <QObject>

	using namespace bb::cascades;

	namespace bb { namespace cascades { class Application; }}

	class ApplicationUI : public QObject
	{
		Q_OBJECT
		Q_STEROID_PROPERTY(QString name, rwn)
	public:
		ApplicationUI(bb::cascades::Application *app);
		virtual ~ApplicationUI() {}
	};

	#endif /* ApplicationUI_HPP_ */

### Q\_STEROID\_DEBUG