package study.coroutine

import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking

fun ex09Continuation() = runBlocking {
    val userService = UserService()
    userService.findUser(1L)
}


interface Continuation {
    suspend fun resumeWith(data: Any?)
}

class UserService {
    private val userProfileRepository = UserProfileRepository()
    private val userImageRepository = UserImageRepository()

    private abstract class FindUserContinuation : Continuation {
        var label = 0
        var profile: Profile? = null
        var image: Image? = null
    }

    suspend fun findUser(userId: Long, continuation: Continuation? = null): UserDto {
        val stateMachine = continuation as? FindUserContinuation ?: object : FindUserContinuation() {
            override suspend fun resumeWith(data: Any?) {
                when (label) {
                    0 -> {
                        profile = data as Profile
                        label = 1
                    }

                    1 -> {
                        image = data as Image
                        label = 2
                    }
                }

                findUser(userId, this)
            }
        }

        when (stateMachine.label) {
            0 -> {
                println("프로필 조회")
                userProfileRepository.findProfile(userId, stateMachine)
            }

            1 -> {
                println("이미지 조회")
                userImageRepository.findImage(stateMachine.profile!!, stateMachine)
            }
        }
        return UserDto(stateMachine.profile!!, stateMachine.image!!)
    }
}

class UserProfileRepository {
    suspend fun findProfile(userId: Long, continuation: Continuation) {
        delay(100L)
        continuation.resumeWith(Profile())
    }
}

class UserImageRepository {
    suspend fun findImage(userId: Profile, continuation: Continuation) {
        delay(100L)
        continuation.resumeWith(Image())
    }
}

class Profile

class Image

data class UserDto(
    val profile: Profile,
    val image: Image,
)
