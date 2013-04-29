Introduction
============

DeathByCaptcha service offers APIs of two types:  HTTP based one and socket
based one, with the latter being recommended for having faster responses,
lower average solving times and overall better performance.  Usually
switching between clients is as easy as changing the client class or package
name.


How to use our DBC API clients
==============================

For the sake of brevity we'll use socket based API in the following examples,
and way to switch to the old HTTP based API will be mentioned.


C#
--

    /* Put your DBC username and password here.  Use DeathByCaptcha.Client
       class instead if you want to use the HTTP based API. */

    DeathByCaptcha.Client3 client =
        new DeathByCaptcha.Client3(username, password);

    /* Upload and try to solve a CAPTCHA.  Put your CAPTCHA image file name,
       or opened file stream, or a vector of bytes, and an optional solving
       timeout (in seconds, defaults to 60) here, and you'll receive
       DeathByCaptcha.Captcha object with the CAPTCHA ID, text (if solved) and
       status, as integer attribute Id, string attribute Text and two boolean
       attributes, Uploaded and Solved respectively. */

    DeathByCaptcha.Captcha = client.Decode(captchaFileName, timeout);

    /* If the CAPTCHA was solved incorrectly, report the fact to the service.
       You can put either CAPTCHA ID or DeathByCaptcha.Captcha object here. */

    client.Report(captcha)


Java
----

    /* Put your DBC username and password here.  Use com.DeathByCaptcha.Client
       class instead if you want to use the HTTP based API. */

    com.DeathByCaptcha.Client3 client =
        new com.DeathByCaptcha.Client3(username, password);

    /* Upload and try to solve a CAPTCHA.  Put your CAPTCHA image file name,
       or opened file stream, or a vector of bytes, and an optional solving
       timeout (in seconds, defaults to 60) here, and you'll receive
       com.DeathByCaptcha.Captcha object with the CAPTCHA ID, text (if solved)
       and status, accessible through getId(), getText() and isUploaded() /
       isSolved() methods respectively. */

    com.DeathByCaptcha.Captcha = client.decode(captchaFileName, timeout);

    /* If the CAPTCHA was solved incorrectly, report the fact to the service.
       You can put either CAPTCHA ID or com.DeathByCaptcha.Captcha object
       here. */

    client.report(captcha)


Perl
----

    # Import DBC client related classes.  Use DeathByCaptcha::Client class if
    # you want to use the HTTP based API.

    use DeathByCaptcha::Client3;

    # Put your DBC username and password here.

    my $client = DeathByCaptcha::Client3->new($username, $password);

    # Upload and try to solve a CAPTCHA.  Put your CAPTCHA image file name and
    # an optional solving timeout (in seconds, defaults to 60) here, you'll
    # receive (ID, text) pair on success

    my ($id, $text) = $client->decode($captcha_file_name, $timeout);

    # If the CAPTCHA was solved incorrectly, report the fact to the service.

    $client->report($id);


PHP 5+
------

    // Import DBC client related classes.  Import 'dbc_client.php' if you want
    // to use the HTTP based API.

    require_once 'dbc_client.3.php';

    // Put your DBC username & password here

    $client = new DeathByCaptcha_Client($username, $password);

    // Upload and try to solve a CAPTCHA.  Put your CAPTCHA image file name
    // or opened file handler, and an optional solving timeout (in seconds,
    // defaults to 60) here, you'll receive (ID, text) pair on success

    list($id, $text) = $client->decode($captcha_file_name, $timeout);

    // If the CAPTCHA was solved incorrectly, report the fact to the service.

    $client->report($id);


Python
------

    # Import DBC client module.  Use dbc_client module if you want to use the
    # HTTP based API.

    import dbc_client3

    # Put your DBC username and password here.

    client = dbc_client3.Client(username, password)
    
    # Upload and try to solve a CAPTCHA.  Put your CAPTCHA image file name
    # or opened file handler, and an optional solving timeout (in seconds,
    # defaults to 60) here, and you'll receive (ID, text) tuple on success.

    id, text = client.decode(captcha_file_name, timeout)

    # If the CAPTCHA was solved incorrectly, report the fact to the service.

    client.report(id)


Visual Basic
------------

    ' Put your DBC username and password here.  Use DeathByCaptcha.Client
    ' class instead if you want to use the HTTP based API.

    Dim client As New DeathByCaptcha.Client3(Username, Password)

    ' Upload and try to solve a CAPTCHA.  Put your CAPTCHA image file name,
    ' or opened file stream, or a vector of bytes, and an optional solving
    ' timeout (in seconds, defaults to 60) here, and you'll receive
    ' DeathByCaptcha.Captcha object with the CAPTCHA ID, text (if solved) and
    ' status as integer attribute Id, string attribute Text and two boolean
    ' attributes, Uploaded and Solved respectively.

    Dim captcha As DeathByCaptcha.Captcha =
        client.Decode(captchaFileName, timeout);

    ' If the CAPTCHA was solved incorrectly, report the fact to the service.
    ' You can put either CAPTCHA ID or DeathByCaptcha.Captcha object here.

    client.Report(captcha)


If you need more fine-grained control over the solving process, or want to use
some custom logic, our API clients offer a few methods ...

To upload a CAPTCHA, call:

    C#/VB:  client.Upload(...);
    Java:   client.upload(...);
    Perl:   $client->upload(...);
    PHP:    $client->upload(...);
    Python: client.upload(...)

The methods accept CAPTCHA file names as the only attribute.  Additionally,
C#/VB and Java methods accept file streams and vectors of bytes; PHP method
accepts file handlers; Python method accepts file objects (StringIO is ok).
The methods return integer CAPTCHA ID on success.

To check an uploaded CAPTCHA status, call:

    C#/VB:  client.GetText(...);
    Java:   client.getText(...);
    Perl:   $client->getText(...);
    PHP:    $client->get_text(...);
    Python: client.get_text(...)

The methods accept integer CAPTCHA ID as the only attribute.  Additionally,
C#/VB and Java methods accept (respectively) DeathByCaptcha.Captcha and
com.DeathByCaptcha.Captcha objects.  The methods return non-empty string
with the CAPTCHA text, is solved.

To remove an unsolved CAPTCHA, call:

    C#/VB:  client.Remove(...);
    Java:   client.remove(...);
    Perl:   $client->remove(...);
    PHP:    $client->remove(...);
    Python: client.remove(...)

The methods accept integer CAPTCHA ID as the only attribute.  Additionally,
C#/VB and Java methods accept (respectively) DeathByCaptcha.Captcha and
com.DeathByCaptcha.Captcha objects.  The methods return boolean status showing
if the CAPTCHA was successfully removed.  Note: you can't remove CAPTCHA
already solved or being solved.  Note: our system marks some invalid or
unreadable CAPTCHA images as incorrect automatically setting its text to a
question mark.  Please, do not forget to check the sanity of the text you're
receiving.

To report a CAPTCHA incorrectly solved, call:

    C#/VB:  client.Report(...);
    Java:   client.report(...);
    Perl:   $client->report(...);
    PHP:    $client->report(...);
    Python: client.report(...)

The methods accept integer CAPTCHA ID as the only attribute.  Additionally,
C#/VB and Java methods accept (respectively) DeathByCaptcha.Captcha and
com.DeathByCaptcha.Captcha objects.  The methods return boolean status showing
if the CAPTCHA was successfully reported.
