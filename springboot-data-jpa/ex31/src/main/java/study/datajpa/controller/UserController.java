package study.datajpa.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import study.datajpa.domain.entity.User;
import study.datajpa.service.UserService;

import java.util.List;

@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/master")
    public List<User> getMaster() {
        return userService.findAll();
    }

    @GetMapping("/slave")
    public List<User> getSlave() {
        return userService.findAllBySlave();
    }
}
