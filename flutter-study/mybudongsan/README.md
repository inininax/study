# MyBudongsan


## iOS 설정 오류 수정
- ios/Podfile 수정
```shell
# 최 상단 해당 구문 추가
platform :ios, '13.0'
```

- pod install
```shell
cd ios
pod install
```

- rebuild
```shell
flutter clean
flutter run
```

## Logger
- logger 설치
```shell
flutter pub add logger
```

- 사용 예시
- [lib/config/logger.dart](lib/config/logger.dart)


## dotenv
- flutter_dotenv 설치
```shell
flutter pub add flutter_dotenv
```

- 사용 예시
- [lib/config/config.dart](lib/config/config.dart)


## Offline
- connectivity_plus 설치
```shell
flutter pub add connectivity_plus
```

- 사용 예시
```dart
  var connectivityResult = await Connectivity().checkConnectivity();
  var isConnect = connectivityResult.contains(ConnectivityResult.mobile) ||
          connectivityResult.contains(ConnectivityResult.wifi);
  
  logger.debug("connectivityResult: $connectivityResult, isConnect: $isConnect");
  
  return isConnect;
```

## Firebase

### Firebase 초기 설정
- Firebase 프로젝트 생성
    - Firebase Console에서 프로젝트 생성

- Firebase SDK 설정
```sheel
export PATH="$PATH":"$HOME/.pub-cache/bin"
npm install -g firebase-tools
dart pub global activate flutterfire_cli
firebase login
flutterfire configure
flutter pub add firebase_core
```

- 설정 완료 시 Firebase Console에서 생성 된 App 확인 가능

- ignore 된 생성 파일 목록
```shell
android/app/google-services.json
ios/Podfile
firebase.json
```

### Firebase Analytics
- firebase_analytics 추가
```shell
flutter pub add firebase_analytics
````

- 기본 설정
```dart
void main() async {
  // ...

  // firebase
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // ...
}
```

- 이벤트 등록
```dart
await FirebaseAnalytics.instance.logEvent(
  name: "test_click",
  parameters: {
    "test_name": title,
  },
).then(
  (result) {
    // ...
  },
);
```


### Firebase Remote Config
- firebase_remote_config 추가
```shell
flutter pub add firebase_remote_config
```

- 기본 설정 및 설정값 불러오기
```dart
class _MainPage extends State<MainPage> {
  final FirebaseRemoteConfig remoteConfig = FirebaseRemoteConfig.instance;

  String welcomeTitle = "";
  bool bannerUse = false;
  int itemHeight = 50;

  @override
  void initState() {
    super.initState();
    remoteConfigInit();
  }

  void remoteConfigInit() async {
    await remoteConfig.fetchAndActivate();

    welcomeTitle = remoteConfig.getString("welcome");
    bannerUse = remoteConfig.getBool("banner");
    itemHeight = remoteConfig.getInt("item_height");
  }
}
```


### Firebase Database
- firebase_database 추가
```shell
flutter pub add firebase_database
```

- 기본 설정
```dart
class _MainPage extends State<MainPage> {
  // ...

  // firebase database
  FirebaseDatabase database = FirebaseDatabase.instance;
  late DatabaseReference _testRef;
  late List<String> testList = List.empty(growable: true);
  
  // ...
}
```

- 데이터 추가
```dart
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () {
          FirebaseDatabase database = FirebaseDatabase.instance;
          DatabaseReference _testRef = database.ref('test');

          _testRef.push().set("""{
  "title": "당신이 좋아하는 애완동물은",
  "question": "당신이 무인도에 도착했는데 마침 떠내려온 상자를 열었을때 보이는 이것은",
  "selects": [
    "생존키트",
    "휴대폰",
    "텐트",
    "무인도에서 살아남기"
  ],
  "answer": [
    "당신은 현실주의 동물은 안키운다!!",
    "당신은 늘 함께 있는 걸 좋아하는 강아지가 딱입니다",
    "당신은 같은 공간을 공유하는 고양이",
    "당신은 낭만을 좋아하는 앵무새"
  ]
}""");
          _testRef.push().set("""{
  "title": "5초 MBTI I/E 편",
  "question": "친구와 함께 간 미술관 당신이라면",
  "selects": [
    "말이 많아짐",
    "생각이 많아짐"
  ],
  "answer": [
    "당신의 성향은 E",
    "당신의 성향은 I"
  ]
}""");
          _testRef.push().set("""{
  "title": "당신은 어떤 사랑을 하고 싶나요",
  "question": "목욕을 할때 가장 먼저 비누칠을 하는 곳은",
  "selects": [
    "머리",
    "상체",
    "하체"
  ],
  "answer": [
    "당신은 자만추를 추천해요",
    "당신은 소개팅을 통한 새로운 사람의 소개를 좋아합니다",
    "당신은 길가다가 우연히 지나친 그런 인연을 좋아합니다"
  ]
}""");
        },
      )
```

