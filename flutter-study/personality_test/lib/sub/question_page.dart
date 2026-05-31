import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:flutter/material.dart';
import 'package:flutterstudy/detail/detail_page.dart';

class QuestionPage extends StatefulWidget {
  final Map<String, dynamic> question;

  const QuestionPage({super.key, required this.question});

  @override
  State<StatefulWidget> createState() {
    return _QuestionPage();
  }
}

class _QuestionPage extends State<QuestionPage> {
  String title = '';
  String question = '';
  List<String> selects = List.empty(growable: true);
  List<String> answers = List.empty(growable: true);
  int selectNumber = -1;

  @override
  void initState() {
    super.initState();

    title = widget.question['title'];
    question = widget.question['question'];

    selects.clear();
    widget.question['selects'].forEach((element) {
      selects.add(element.toString());
    });

    answers.clear();
    widget.question['answer'].forEach((element) {
      answers.add(element.toString());
    });
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> widgets = List<Widget>.generate(
      selects.length,
      (int index) => SizedBox(
        height: 100,
        child: Column(
          children: [
            Text(selects[index]),
            Radio(
              value: index,
              groupValue: selectNumber,
              onChanged: (value) {
                setState(() {
                  selectNumber = index;
                });
              },
            )
          ],
        ),
      ),
    );

    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: Column(
        children: [
          Text(question),
          Expanded(
            child: ListView.builder(
              itemCount: widgets.length,
              itemBuilder: (context, index) {
                return widgets[index];
              },
            ),
          ),
          selectNumber == -1
              ? Container()
              : ElevatedButton(
                  onPressed: () async {
                    await FirebaseAnalytics.instance.logEvent(
                      name: "personal_select",
                      parameters: {
                        "test_name": title,
                        "select": selectNumber,
                      },
                    ).then(
                      (result) => {
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(
                            builder: (context) {
                              return DetailPage(
                                answer: answers[selectNumber],
                                question: question,
                              );
                            },
                          ),
                        ),
                      },
                    );
                  },
                  child: const Text('성격 보기'),
                ),
        ],
      ),
    );
  }
}
