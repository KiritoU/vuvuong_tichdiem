class Constants:
    # Values
    DEFAULT_MONTHLY_CHECKIN_REWARD = {
        # days: coin
        1: 3,
        3: 10,
        7: 30,
        14: 100,
        21: 150,
        28: 200,
    }

    # Success
    SUCCESS = "Thành công"
    SIGNUP_SUCCESS = "Đăng ký thành công"
    LOGIN_SUCCESS = "Đăng nhập thành công"
    ANSWER_SUCCESS = "Gửi câu trả lời thành công"
    USER_INFO = "Thông tin của bạn"
    USER_CHECKIN = "Thông tin điểm danh của bạn"
    USER_CHECKIN_SUCCESS = "Điểm danh thành công"
    USER_DAILY_QUESTIONS = "Danh sách câu hỏi hàng ngày của bạn"
    USER_LIST_CODES = "Danh sách code của bạn"
    USER_EXCHANGE_CODE_SUCCESS = "Đổi code thành công"
    USER_LIST_ROTATION_LUCK_REWARDS = "Danh sách phần thưởng cho vòng quay may mắn"
    USER_ROTATE_SUCCESS = "Phần thưởng vòng quay lượt này của bạn"
    USER_RECEIVE_MONTHLY_CHECKIN_REWARD_SUCCESS = "Nhận thưởng mốc {} ngày thành công"

    # Failure
    LOGIN_FAILED = (
        "Tên đăng nhập, mật khẩu hoặc thiết bị đăng nhập không đúng. Vui lòng thử lại!"
    )
    USER_INFO_FAILED = "Lấy thông tin của bạn thất bại"
    USERNAME_EXIST = "Tên đăng nhập đã tồn tại"
    EMAIL_EXIST = "Email đã tồn tại"
    DEVICE_EXIST = "Thiết bị đã được sử dụng để đăng ký"
    PERMISSION_DENIED = "Bạn không thể thực hiện hành động này"
    UNAUTHORIZED = "Thông tin xác thực không chính xác"
    USER_ALREADY_CHECKED_IN = "Đã điểm danh ngày hôm nay"
    COIN_PRICE_LTE_ZERO = "Không thể đổi code với giá trị nhỏ hơn hoặc bằng 0 coin"
    CODE_WITH_COIN_PRICE_DOES_NOT_EXIST = "Hiện không có code trị giá {} coin"
    NOT_ENOUGH_COIN = "Không đủ coin để thực hiện hành động này"
    MONTHLY_CHECKIN_REWARD_NOT_FOUND = "Không có phần thưởng điểm danh cho mốc {} ngày"
    NOT_ENOUGH_CHECKED_IN_COUNT = "Bạn chưa đạt đủ mốc checkin {} ngày"
    RECEIVED_MONTHLY_CHECKIN_REWARD = "Bạn đã nhận thưởng cho mốc {} ngày"

    # History
    HISTORY_RECEIVE_INVITATION_REWARD = "Nhận quà giới thiệu"
    HISTORY_RECEIVE_QUIZ_REWARD = "Nhận coin trả lời Quiz"
    HISTORY_EXCHANGE_CODE = "Đổi code {} trị giá {} coin"
    HISTORY_RECEIVE_CODE_FROM_ROTATION_LUCK = "Nhận code {} từ vòng quay may mắn"
    HISTORY_MONTHLY_CHECKIN_REWARD = "Nhận quà điểm danh mốc {} ngày"
    HISTORY_RORATE_LUCK_WHEEL = "Tham gia vòng quay may mắn với {} coin"
    HISTORY_RECEIVE_COIN_FROM_ROTATION_LUCK = "Nhận {} coin từ vòng quay may mắn"


constants = Constants()
